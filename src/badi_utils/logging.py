from django.conf import settings

from django.apps import apps as django_apps

from django.utils.translation import gettext_lazy as _

Log = django_apps.get_model(getattr(settings, "LOG_MODEL"), require_ready=False)


def log(user, priority, action, status, my_object=None, field=None, text=None):
    lg = Log()
    lg.user = user
    lg.priority = priority
    lg.status = status
    if text:
        lg.title = _('custom')
        lg.description = text
    else:
        if action == 1:
            lg.title = _('login')
            lg.description = 'کاربر ' + str(user) + ' به سامانه وارد شد.'
        elif action == 2:
            lg.title = _('logout')
            lg.description = 'کاربر ' + str(user) + ' از سامانه خارج شد.'
        elif action == 3:
            lg.title = 'ایجاد رکورد'
            lg.description = "کاربر " + str(user) + " " + str(my_object._meta.verbose_name) + "'" + str(
                field) + "'" + " را اضافه کرد."
        elif action == 4:
            lg.title = 'ویرایش رکورد'
            lg.description = "کاربر " + str(user) + " " + str(my_object._meta.verbose_name) + "'" + str(
                field) + "'" + " را ویرایش کرد."
        elif action == 5:
            lg.title = _("Delete")
            lg.description = "کاربر " + str(user) + " " + str(my_object._meta.verbose_name) + "'" + str(
                field) + "'" + " را حذف کرد."
    lg.save()
    return lg
