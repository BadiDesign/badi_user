import datetime
import random
import string
from datetime import timedelta

from badi_utils.email import Email
from badi_utils.errors import BadiErrorCodes
from badi_utils.validations import PersianValidations, BadiValidators
from django.contrib.auth import login, validators
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.http import JsonResponse, Http404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from badi_utils.dynamic_api import DynamicModelApi, InCaseSensitiveTokenObtainPairSerializer
from badi_utils.logging import log
from badi_utils.responses import ResponseOk, ResponseNotOk
from badi_utils.utils import random_with_N_digits, permissions_json
from rest_framework_simplejwt.views import TokenRefreshView

from badi_user.api.serializers import UserSerializer, GroupSerializer, MemberSerializer
from badi_user.filter import UserListFilter, MemberListFilter
from badi_user.models import Token
from django.utils.translation import gettext_lazy as _
from badi_utils.sms import IpPanelSms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(DynamicModelApi):
    columns = ['id', 'username', 'first_name', 'last_name', 'mobile_number', 'is_admin', 'is_active', ]
    order_columns = ['id', 'username', 'first_name', 'last_name', 'mobile_number', 'is_admin', 'is_active', ]
    model = User
    queryset = User.objects.filter(is_admin=True)
    serializer_class = UserSerializer
    custom_perms = {
        'self': True
    }
    switches = {
        'is_active': {
            'true': ' ',
            'false': ' ',
        }
    }

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.action == 'datatable':
            return UserListFilter(self.request.POST).qs.filter(is_admin=True)
        return super().filter_queryset(qs)

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        user = User.objects.filter(pk=int(self.kwargs['pk'])).first()
        if user:
            res.data['image'] = user.get_image()
        return res

    @action(methods=['get'], detail=False)
    def self(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['put'], detail=False, url_path='change_state/(?P<pk>[^/.]+)')
    def change_state(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()

        return JsonResponse({
            'message': 'با موفقیت {0} شد'.format('فعال' if user.is_active else 'غیرفعال')
        })


BADI_AUTH_CONFIG = {
    "resend": {
        "is_active": True,
        "class": IpPanelSms,
        "user_find_key": "username",
        "token_key": "phone",
        "user_key": "mobile_number",
        "errors": {
            "404": _("No active user found")
        }
    },
    "verify": {
        "is_active": True,
        "user_find_key": "username",
        "token_key": "phone",
        "user_key": "mobile_number",
    },
    "register": {
        "is_active": True,
        "user_find_key": "username",
        "token_key": "phone",
        "user_key": "mobile_number",
        "email_active": False,
        "mobile_number_active": True,
        "mobile_number_validator": PersianValidations.phone_number,
        "email_panel": PersianValidations.phone_number,
        "sms_panel": IpPanelSms,
        "username_validator": BadiValidators.username,
    },
    "login": {
        "is_active": True,
        "type": "username_password",
        "auto_create": True,
        "login_to_django": True,
        "user_key": "username",
        "email_panel": Email.send_login_token,
        "sms_panel": IpPanelSms,
        "username_validator": PersianValidations.phone_number,
    },
}


class LoginAuth:
    @staticmethod
    def _login_with_email_token(request, config):
        email = request.data.get('username')
        code = request.data.get('code')
        if BadiValidators.is_mail(email):
            user, is_created = User.objects.get_or_create(email=email,
                                                          defaults={"username": email})
        else:
            return ResponseNotOk(reason='Invalid Email!')
        if code:
            if user.token and user.token.is_enabled():
                if code == user.token.token:
                    user.token.is_accepted = True
                    user.token.save()
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                else:
                    return ResponseNotOk(reason='Invalid Code!')
        else:
            if user:
                if not user.email:
                    return ResponseNotOk(reason='Email not Found!')
                if user.token and user.token.is_enabled():
                    return ResponseOk(detail='Code Recently sent to your email! please check Inbox and Spam mails!')
                else:
                    tkn = Token(token=random_with_N_digits(5), mail=user.email,
                                last_send=datetime.datetime.now())
                    tkn.save()
                    send_state = Email.send(tkn.token, tkn.mail)
                    if not send_state:
                        return ResponseNotOk(reason='Email Sent Failed! please Check your Email!')

                user.token = tkn
                user.save()
                return ResponseOk(detail='Code Sent to your Email!')

            raise InvalidToken()

    @staticmethod
    def _login_with_sms_token(request, config):
        user_key = config.get("user_key", "mobile_number")
        data = request.data.get(user_key)
        code = request.data.get('code')
        if not config.get("username_validator")(data):
            return ResponseNotOk(reason=_(BadiErrorCodes.phone))
        if config['auto_create']:
            defaults = {"username": data}
            user, is_created = User.objects.get_or_create(**{user_key: data}, defaults=defaults)
        else:
            user = User.objects.filter(mobile_number=data)
            if not user:
                return ResponseNotOk(reason=_(BadiErrorCodes.not_found))
        if code:
            if user.token and user.token.is_enabled():
                if code != user.token.token:
                    return ResponseNotOk(reason=BadiErrorCodes.wrong_code)
                user.token.is_accepted = True
                user.token.save()
                if config.get("login_to_django"):
                    login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
        else:
            if not user.mobile_number:
                return ResponseNotOk(reason=BadiErrorCodes.not_found)
            if user.token and user.token.is_enabled():
                return ResponseOk(detail='کد تایید شماره تماس که برای شما ارسال شده را وارد کنید!')
            else:
                tkn = Token(token=random_with_N_digits(5), phone=user.mobile_number,
                            last_send=datetime.datetime.now())
                tkn.save()
                config.get("sms_panel")(tkn.phone).send_verify_code(tkn.token)
            user.token = tkn
            user.save()
            return ResponseOk(detail=_("Code sent to ") + data)

        raise InvalidToken()

    @staticmethod
    def _login_with_username_password_token(request, config):
        serializer = TokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = request.data.get('username')
            dashboard_login = request.data.get('dashboard_login')
            user = User.objects.filter(username=username).first()
            if user.is_superuser:
                user.is_admin = True
                user.save()
            if dashboard_login and not user.is_admin:
                log(user, 1, 1, False)
                return ResponseNotOk(reason='You dont have Permission to access Dashboard!')
            else:
                login(request, user)
            log(user, 1, 1, True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ViewSet, LoginAuth):
    permission_classes = []

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        config = BADI_AUTH_CONFIG['login']
        if config["type"] == "email_token":
            return self._login_with_email_token(request, config)
        if config["type"] == "sms_token":
            return self._login_with_sms_token(request, config)
        if config["type"] == "username_password":
            return self._login_with_username_password_token(request, config)

        return ResponseNotOk()

    @action(methods=['post'], detail=False)
    def register(self, request, *args, **kwargs):
        config = BADI_AUTH_CONFIG['register']
        if not config['is_active']:
            return Http404()
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        username = self.request.data.get('username')
        mobile_number = self.request.data.get('mobile_number')
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        if config['username_validator'] and not config['username_validator'](username):
            return Response({'username': [_('Invalid username'), ]}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).first():
            return Response({'username': [_('This username already taken'), ]}, status=status.HTTP_400_BAD_REQUEST)
        if config['mobile_number_active']:
            if User.objects.filter(mobile_number=mobile_number).first():
                return Response({'mobile_number': [_('This mobile number already registered'), ]},
                                status=status.HTTP_400_BAD_REQUEST)
            if not config['mobile_number_validator'](mobile_number):
                return Response({'mobile_number': ['Invalid mobile number']}, status=status.HTTP_400_BAD_REQUEST)
        if config['email_active']:
            if User.objects.filter(email=email).first():
                return Response({'email': [_('This mobile number already registered'), ]},
                                status=status.HTTP_400_BAD_REQUEST)
            if not config['email_validator'](email):
                return Response({'email': ['Invalid mobile number']},
                                status=status.HTTP_400_BAD_REQUEST)
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.password = make_password(password)
        user.username = username
        token = Token()
        if config['mobile_number_active']:
            user.mobile_number = mobile_number
            token.phone = mobile_number
        if config['email_active']:
            user.email = email
            token.email = email
        user.save()
        token.token = random_with_N_digits(5)
        token.last_send = timezone.now()
        if config['sms_panel']:
            config['sms_panel'](mobile_number).send_verify_code(token.token)
        if config['email_panel']:
            config['email_panel'](email).send_verify_code(token.email)
        token.save()
        user.token = token
        user.save()
        return ResponseOk()

    @action(methods=['post'], detail=False)
    def resend(self, request, *args, **kwargs):
        config = BADI_AUTH_CONFIG['resend']
        if not config['is_active']:
            return Http404()
        data = request.data.get(config['user_find_key'])
        user = User.objects.filter(**{config['user_find_key']: data}).first()
        if not user:
            return ResponseNotOk(reason=config['errors']['404'])
        user_attr = getattr(user, config['user_find_key'])
        token = Token.objects.filter(**{config['token_key']: user_attr}).last()
        if token and token.is_active():
            if token.is_possible_resend():
                config['class'](user_attr).send_verify_code(token.token)
                token.last_send = datetime.datetime.now()
                token.save()
            else:
                return ResponseNotOk(reason=_(BadiErrorCodes.sms_send_recently))
        else:
            token = Token()
            token.token = random_with_N_digits(5)
            setattr(token, config['token_key'], user_attr)
            token.last_send = datetime.datetime.now()
            config['class'](user.mobile_number).send_verify_code(token.token)
            token.save()

        return ResponseOk()

    @action(methods=['post'], detail=False)
    def verify(self, request, *args, **kwargs):
        config = BADI_AUTH_CONFIG['verify']
        if not config['is_active']:
            return Http404()
        data = request.data.get(config['user_find_key'])
        code = request.data.get('code')
        token = Token.objects.filter(**{config['user_find_key']: data}, is_accepted=False).last()
        if not token:
            return ResponseNotOk(reason=_(BadiErrorCodes.not_found))
        if not token.is_active():
            return ResponseNotOk(reason=_(BadiErrorCodes.expired))
        if token.token != code:
            return ResponseNotOk(reason=_(BadiErrorCodes.wrong_code))
        user = User.objects.filter(**{config['user_key']: data}).first()
        refresh = RefreshToken.for_user(user)
        token.is_accepted = True
        token.save()
        Token.objects.filter(created_at__lt=datetime.datetime.now() - timedelta(hours=24)).delete()
        login(self.request, user)
        return ResponseOk(detail={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    @action(methods=['put'], detail=False)
    def change_password(self, request, *args, **kwargs):
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        repeat_password = self.request.data.get('repeat_password')
        if not self.request.user.is_authenticated:
            return JsonResponse({
                'new_password': ['بنظر می رسد مشکلی پیش آمده دوباره وارد شوید!']
            }, status=HTTP_401_UNAUTHORIZED)
        errors = {}

        if check_password(old_password, self.request.user.password):
            user = self.request.user
            if new_password == repeat_password:
                self.request.user.password = make_password(new_password)
                self.request.user.save()
                login(request, user)
                log_text = 'کاربر {0} رمز عبور خود را تغییر داد!'.format(user.username)
                log(request.user, 1, 3, True, text=log_text)
                return JsonResponse({})
            else:
                errors['new_password'] = []
                errors['new_password'].append('رمز عبور با تکرار آن مطابقت ندارد')
        else:
            errors['old_password'] = []
            errors['old_password'].append('رمز عبور فعلی اشتباه است')

        return JsonResponse(errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def forgot_password(self, req, *args, **kwargs):
        mobile_number = self.request.data.get('mobile_number')
        user = User.objects.filter(mobile_number=mobile_number).first()
        if not user:
            return JsonResponse({'mobile_number': ['کاربری با شماره تماس وارد شده وجود ندارد!']},
                                status=HTTP_400_BAD_REQUEST)

        phone_number = self.request.data.get('mobile_number')
        HTTP_ORIGIN = req.META.get('HTTP_ORIGIN')
        if phone_number and len(phone_number) == 11:
            user = User.objects.filter(mobile_number=phone_number).first()
            if user:
                if user.token and user.token.is_enabled():
                    return JsonResponse({'mobile_number': ['شما به تازگی درخواست داده اید!']},
                                        status=HTTP_400_BAD_REQUEST)
                hash_code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
                token = Token()
                token.user = user
                token.last_send = datetime.datetime.now()
                token.is_forgot = True
                token.token = hash_code
                token.save()
                user.token = token
                user.save()
                token_id_hash = token.pk * 8569 - 1330
                text = f'{HTTP_ORIGIN}/forgot_password/{token_id_hash}/{hash_code}'
                print(f'لینک تغییر رمز عبور: %0D%0A {text}')
                Sms.link(user.mobile_number, token_id_hash, hash_code)
                return ResponseOk({})

            else:
                return JsonResponse({'mobile_number': ['کاربری با شماره تماس وارد شده وجود ندارد!']},
                                    status=HTTP_400_BAD_REQUEST)

        return JsonResponse({'mobile_number': ['مشکلی پیش آمده است!']}, status=HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def refresh(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False)
    def forgot_change_password(self, req, *args, **kwargs):

        new_password = req.data.get('new_password')
        token_id = req.data.get('token_id')
        hash_code = req.data.get('hash_code')

        if new_password and len(new_password) > 5 and token_id and hash_code:
            token = Token.objects.filter(pk=(int(token_id) + 1330) / 8569, token=hash_code, is_forgot=True,
                                         is_accepted=False).first()
            if not token:
                return JsonResponse({'': ['این شناسه تغییر رمز عبور منقضی شده است لطفا دوباره تلاش کنید!']},
                                    status=HTTP_400_BAD_REQUEST)
            if token and token.is_enabled():
                user = token.user.first()
                user.password = make_password(new_password)
                user.save()
                token.is_accepted = True
                token.save()
                user.token = None
                user.save()
                return ResponseOk()
            else:
                return JsonResponse({'': ['بنظر می رسد این شناسه تغییر رمز عبور منقضی شده است لطفا دوباره تلاش کنید!']},
                                    status=HTTP_400_BAD_REQUEST)

        return JsonResponse({'': ['بنظر می رسد این شناسه تغییر رمز عبور منقضی شده است لطفا دوباره تلاش کنید!']},
                            status=HTTP_400_BAD_REQUEST)


class GroupViewSet(DynamicModelApi):
    columns = ['id', 'name']
    order_columns = ['id', 'name']
    model = Group
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    custom_perms = {
        'datatable': 'can_manage_user'
    }

    @action(methods=['get'], detail=False)
    def permissions(self, request, *args, **kwargs):
        perms = permissions_json()
        return Response(perms)


class MemberViewSet(DynamicModelApi):
    columns = ['id', 'id', 'picture', 'username', 'first_name', 'last_name', 'amount', ]
    order_columns = ['id', 'id', 'picture', 'username', 'first_name', 'last_name', 'amount', ]
    model = User
    queryset = User.objects.filter(is_admin=False)
    serializer_class = MemberSerializer
    custom_perms = {
        'self': True,
        'update_self': True,
    }

    def filter_queryset(self, qs):
        if self.action == 'datatable':
            return MemberListFilter(self.request.POST).qs.filter(is_admin=False)
        return super().filter_queryset(qs)

    def retrieve(self, request, *args, **kwargs):
        if 'retrieve' in self.disables_views:
            return Http404()
        res = super().retrieve(request, *args, **kwargs)
        user = User.objects.filter(pk=int(self.kwargs['pk'])).first()
        if user:
            res.data['image'] = user.get_image()
        return res

    @action(methods=['get'], detail=False)
    def self(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.request.user).data)

    @action(methods=['put'], detail=False)
    def update_self(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['put'], detail=False)
    def change_password(self, request, *args, **kwargs):
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        repeat_password = self.request.data.get('repeat_password')

        errors = {}

        if check_password(old_password, self.request.user.password):
            user = self.request.user
            if new_password == repeat_password:
                self.request.user.password = make_password(new_password)
                self.request.user.save()
                login(request, user)
                log_text = 'کاربر {0} رمز عبور خود را تغییر داد!'.format(user.username)
                log(request.user, 1, 3, True, text=log_text)
                return JsonResponse({})
            else:
                errors['new_password'] = []
                errors['new_password'].append('رمز عبور با تکرار آن مطابقت ندارد')
        else:
            errors['old_password'] = []
            errors['old_password'].append('رمز عبور فعلی اشتباه است')

        return JsonResponse(errors, status=HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=False)
    def admin_change_password(self, request, *args, **kwargs):
        user = User.objects.filter(pk=int(self.request.data.get('user'))).first()
        if user:
            password = self.request.data.get('password')
            repeat_password = self.request.data.get('repeat_password')
            if repeat_password == password:
                user.password = make_password(password)
                user.save()
                return ResponseOk()
            else:
                return ResponseNotOk()
        else:
            return ResponseNotOk()

    def render_column(self, row, column):
        if column == 'transactions__count':
            return row.transactions.count()
        return super().render_column(row, column)
