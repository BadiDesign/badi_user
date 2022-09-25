# Create your views here.
from django.shortcuts import render
from django.views import View

from plugins.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from plugins.utils import LoginRequiredMixin
from user.filter import UserListFilter
from user.models import User
from user.ui.forms import user_form


class UserListView(DynamicListView):
    model = User
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'شماره تماس', 'مدیر', 'فعال', ]

    def get_extra_context(self, context):
        context['filters'] = UserListFilter(self.request.POST)
        return super().get_extra_context(context)


class UserCreateView(DynamicCreateView):
    """
    برای ایجاد یک کاربرجدید که عضو کاشف هست  در سامانه از این کلاس استفاده میشود

    Arguments:
        form_class(UserCreateForm):
          فرمی که کلاس از آن استفاده میشود
        template_name(str):
           آردس تمپلت مورد استفاده در کلاس
        success_url(str):
           آدرس url که در صورت موفق بودن فرم، کاربر به آن هدایت خواهد شد
    """
    model = User
    form = user_form(
        ['username', 'password', 'first_name', 'last_name', 'is_admin', 'mobile_number', ])
    datatableEnable = False

    def get_extra_context(self, context):
        context['back'] = '/user/list'
        return context


class UserUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
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
