# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render
from django.views import View

from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_utils.utils import LoginRequiredMixin
from badi_user.filter import UserListFilter
from badi_user.models import User
from badi_user.ui.forms import user_form


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
    template_name = 'login.html'

    def form_valid(self, form):
        return Http404
