from logging import log
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_utils.utils import LoginRequiredMixin
from badi_user.filter import UserListFilter
from badi_user.models import Token
from badi_user.ui.forms import user_form
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListView(DynamicListView):
    model = User
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'شماره تماس', 'مدیر', 'فعال', ]

    def get_extra_context(self, context):
        context['filters'] = UserListFilter(self.request.POST)
        return super().get_extra_context(context)


class UserCreateView(DynamicCreateView):
    model = User
    form = user_form(
        ['username', 'password', 'first_name', 'last_name', 'is_admin', 'mobile_number', ])
    datatableEnable = False

    def get_extra_context(self, context):
        context['back'] = '/user/list'
        return context


class UserUpdateView(DynamicUpdateView):
    model = User
    form = user_form(
        ['username', 'password', 'first_name', 'last_name', 'is_admin', 'mobile_number', ], update=True)
    success_url = '/user/list'


class ChangePasswordViewTemplateView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title': 'تغییر رمز عبور'
        }
        return render(request, 'user/change_password.html', context)


class UserLoginView(LoginView):
    template_name = 'login-theme/login-1.html'

    def form_valid(self, form):
        return Http404


class ChangePasswordForgot(View):

    def get(self, req, token_id, hash_code, *args):
        token = Token.objects.filter(pk=(int(token_id) + 1330) / 8569, token=hash_code, is_forgot=True,
                                     is_accepted=False).first()
        if token and token.is_enabled():
            return render(req, 'user/change_password.html', {
                'dont_ask_password': True,
                'disable_nav': True,
                'token_id': token_id,
                'hash_code': hash_code
            })
        else:
            return redirect('custom_login')


class UserLogout(LoginRequiredMixin, View):

    def get(self, request):
        request.user.last_logout = timezone.now()
        request.user.last_activity = timezone.now()
        request.user.save()
        log(request.user, 1, 2, True)
        logout(request)

        return redirect('/')
