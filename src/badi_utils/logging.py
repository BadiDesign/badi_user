from django.conf import settings

from django.apps import apps as django_apps

from django.utils.translation import gettext_lazy as _

Log = django_apps.get_model(getattr(settings, "LOG_MODEL", "badi_user.Log"), require_ready=False)


def log(user, priority, action, status, my_object=None, field=None, text=None):
    lg = Log()
    lg.user = user
    lg.priority = priority
    lg.status = status
    if text:
        lg.title = _('custom')
        lg.description = text
    else:
        user_str = str(user)
        field_str = str(field)
        verbose_name = ''
        user_did = _("User") + ' (' + user_str + ") "
        if action == 1:
            lg.title = _('login')
            lg.description = user_did + _("Logged in")
        elif action == 2:
            lg.title = _('logout')
            lg.description = user_did + _("Logged out")
        else:
            verbose_name = str(my_object._meta.verbose_name)
        if action == 3:
            lg.title = _('Create')
            lg.description = user_did + _("Added") + ' ' + verbose_name + " (" + field_str + ") "
        elif action == 4:
            lg.title = _('Update')
            lg.description = user_did + _("Updated") + ' ' + verbose_name + " (" + field_str + ")"
        elif action == 5:
            lg.title = _("Delete")
            lg.description = user_did + _("Removed") + ' ' + verbose_name + " (" + field_str + ")"
    lg.save()
    return lg
