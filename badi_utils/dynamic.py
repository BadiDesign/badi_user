from django import forms
from django.conf import settings
from django.contrib import messages
from django.db import models
from django.db.models import Q, Model
from django.forms import ModelForm
from django.http import HttpResponse, Http404
from django.urls import path
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from .date_calc import custom_change_date
from .logging import log
from .utils import LoginRequiredMixin, CustomPermissionRequiredMixin
from django.utils.translation import gettext_lazy as _

DISABLE_FORM_SUBMIT = getattr(settings, "DISABLE_FORM_SUBMIT", True)


def get_model_api_url(model: Model, view):
    if hasattr(model, "get_api_url"):
        url = model.get_api_url(view)
        if url:
            return url
    meta_string = str(model._meta)
    model_name = meta_string.split('.')
    if len(model_name) > 1:
        return '/api/v1/' + model_name[1] + '/'
    return '/api/v1/' + meta_string.replace('.', '/') + '/'


def multi_generator_url(model: Model, create=None, datatable=None, update=None, delete=None, add_model_to_url=True):
    # Use:
    #     urlpatterns = [] + multi_generator_url(Model,create=CreateView,update=UpdateView)
    response = []
    model_name = str(model._meta).split('.')[1]
    if create:
        response.append(path(model_name + "/create", create.as_view(), name=model_name + "_create"))
    if update:
        response.append(
            path(model_name + "/update/<int:pk>", update.as_view(), name=model_name + "_update"))
    if delete:
        response.append(
            path(model_name + "/delete/<int:pk>", delete.as_view(), name=model_name + "_delete"))
    if datatable:
        response.append(
            path(model_name + "/datatable", datatable.as_view(), name=model_name + "_datatable"))
    return response


def generate_url(model: Model, create=None, datatable=None, update=None, detail=None, list=None, delete=None, view=None,
                 add_model_to_url=True):
    # Use:
    #     urlpatterns = [generate_url(Model,create=CreateView), ]
    model_name = str(model._meta).split('.')[1]
    model_url = model_name + '/' if add_model_to_url else ''
    if create:
        return path(model_url + "create", create.as_view(), name=model_name + "_create")
    if detail:
        return path(model_url + "detail/<int:pk>", detail.as_view(), name=model_name + "_detail")
    if view:
        return path(model_url + "list", view.as_view(), name=model_name + "_list")
    if update:
        return path(model_url + "update/<int:pk>", update.as_view(), name=model_name + "_update")
    if delete:
        return path(model_url + "delete/<int:pk>", delete.as_view(), name=model_name + "_delete")
    if datatable:
        return path(model_url + "datatable", datatable.as_view(), name=model_name + "_datatable")
    if list:
        return path(model_url + "list", list.as_view(), name=model_name + "_list")
    raise Exception('Generate url Error')


def model_to_path(model):
    def create(_models):
        class A(SettingCreateView):
            model = _models
            template_name = 'shared/dynamic/create.html'

        return A

    def update(_models):
        class A(SettingUpdateView):
            model = _models
            template_name = 'shared/dynamic/update.html'

        return A

    split_name = str(model._meta).split('.')[1]
    return [
        path(split_name + '/create', create(model)().as_view(), name=split_name + "_create"),
        path(split_name + '/update/<int:pk>', update(model)().as_view(), name=split_name + "_update"),
    ]


def dynamic_form(model_class, get_fields=None, form_fields_config=None, just_data=None, exclude_fields=None):
    """
        این تابع مدل و فیلد ها رو درصورت کاستومایز دریافت میکند و فرم آن را میسازد
    """

    if get_fields is None:
        get_fields = []
    if exclude_fields is None:
        exclude_fields = []
    labels = []
    required = []
    classes = []
    field_names = []
    types = []
    errors = {}
    if not get_fields:
        for field in model_class._meta.fields:
            if field.attname not in ['id', 'created_at', 'updated_at'] + exclude_fields:
                controller = {'class': 'form-control'}
                if isinstance(field, models.DateField):
                    controller['class'] = 'form-control date'
                    controller['autocomplete'] = 'off'
                elif isinstance(field, models.FloatField):
                    controller['step'] = "0.01"
                elif isinstance(field, models.DateTimeField):
                    controller['class'] = 'form-control date-time'
                    controller['autocomplete'] = 'off'
                elif isinstance(field, models.BigIntegerField):
                    controller['class'] = 'form-control currency'
                    controller['autocomplete'] = 'off'

                get_fields.append(field.attname.replace('_id', ''))
                field_names.append(field.attname.replace('_id', ''))
                if form_fields_config and form_fields_config.get(field.attname.replace('_id', '')):
                    if isinstance(field, models.BigIntegerField):
                        types.append(forms.CharField())
                    else:
                        types.append(
                            form_fields_config.get(field.attname.replace('_id', '')).get(
                                'type')) if form_fields_config.get(
                            field.attname.replace('_id', '')).get('type') else forms.CharField() if isinstance(field,
                                                                                                               models.DateField) or isinstance(
                            field, models.DateTimeField) else types.append(None)
                    current_field = form_fields_config.get(field.attname.replace('_id', ''))
                    labels.append(current_field.get('label') if current_field.get('label') else field.verbose_name)
                    required.append(current_field.get('required') if current_field.get('required') else not field.blank)
                    classes.append(
                        current_field.get('class') if current_field.get('class') else controller)
                    errors[field.attname.replace('_id', '')] = current_field.get('errors') if current_field.get(
                        'errors') else {
                        'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                        'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                        'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                    }
                else:
                    labels.append(field.verbose_name)
                    required.append(not field.blank)
                    types.append(forms.CharField() if isinstance(field, models.DateField) or isinstance(field,
                                                                                                        models.BigIntegerField) or isinstance(
                        field,
                        models.DateTimeField) else None)
                    classes.append(controller)
                    errors[field.attname.replace('_id', '')] = {
                        'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                        'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                        'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                    }
        for field in model_class._meta.many_to_many:
            get_fields.append(field.attname)
            field_names.append(field.attname)
            labels.append(field.verbose_name)
            types.append(None)
            if form_fields_config and form_fields_config.get(field.attname.replace('_id', '')):
                required.append(
                    form_fields_config.get(field.attname.replace('_id', '')).get('required') if form_fields_config.get(
                        field.attname.replace('_id', '')).get('required') else False)
            else:
                required.append(False)
            classes.append({'class': 'form-control'})
            errors[field.attname] = {
                'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
            }
    else:
        for field in model_class._meta.fields:
            if field.attname not in ['id', 'created_at', 'updated_at'] + exclude_fields:
                if field.attname.replace('_id', '') in get_fields:
                    controller = {'class': 'form-control'}
                    if isinstance(field, models.DateField):
                        controller['class'] = 'form-control date'
                        controller['autocomplete'] = 'off'
                    elif isinstance(field, models.FloatField):
                        controller['step'] = "0.01"
                    elif isinstance(field, models.DateTimeField):
                        controller['class'] = 'form-control date-time'
                        controller['autocomplete'] = 'off'
                    elif isinstance(field, models.BigIntegerField):
                        controller['class'] = 'form-control currency'
                        controller['autocomplete'] = 'off'

                    # get_fields.append(field.attname.replace('_id', ''))
                    field_names.append(field.attname.replace('_id', ''))
                    if form_fields_config and form_fields_config.get(field.attname.replace('_id', '')):
                        types.append(
                            form_fields_config.get(field.attname.replace('_id', '')).get(
                                'type') if form_fields_config.get(
                                field.attname.replace('_id', '')).get('type') else forms.CharField() if isinstance(
                                field,
                                models.DateField) or isinstance(
                                field,
                                models.BigIntegerField) or isinstance(
                                field, models.DateTimeField) else None)
                        current_field = form_fields_config.get(field.attname.replace('_id', ''))
                        labels.append(current_field.get('label') if current_field.get('label') else field.verbose_name)
                        required.append(
                            current_field.get('required') if current_field.get('required') else not field.blank)
                        classes.append(
                            current_field.get('class') if current_field.get('class') else controller)
                        errors[field.attname.replace('_id', '')] = current_field.get('errors') if current_field.get(
                            'errors') else {
                            'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                            'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                            'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                        }
                    else:
                        types.append(forms.CharField() if isinstance(field, models.DateField) or isinstance(field,
                                                                                                            models.BigIntegerField) or isinstance(
                            field,
                            models.DateTimeField) else None)
                        labels.append(field.verbose_name)
                        required.append(not field.blank)
                        classes.append(controller)
                        errors[field.attname.replace('_id', '')] = {
                            'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                            'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                            'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                        }
        for field in model_class._meta.many_to_many:
            if field.attname in get_fields:
                get_fields.append(field.attname)
                field_names.append(field.attname)
                types.append(None)
                labels.append(field.verbose_name)
                required.append(False)
                classes.append({'class': 'form-control'})
                errors[field.attname] = {
                    'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                    'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                    'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                }
    if just_data == True:
        return {
            'model': model_class,
            'fields': get_fields,
            'error_messages': errors,
            'labels': labels,
            'required': required,
            'classes': classes,
            'field_names': field_names,
            'type': types,
        }

    class ModelFormCreator(ModelForm):

        class Meta:
            model = model_class
            fields = get_fields
            error_messages = errors

        def __init__(self, *args, **kwargs):
            super(ModelFormCreator, self).__init__(*args, **kwargs)

            for key, field in enumerate(field_names):
                if types and types[key]:
                    self.fields[field] = types[key]
                self.fields[field].label = labels[key]
                self.fields[field].required = required[key]
                self.fields[field].widget.attrs = classes[key]
                self.fields[field].widget.attrs['placeholder'] = labels[key] + ' را وارد کنید ...'

    return ModelFormCreator


class DynamicListView(LoginRequiredMixin, CustomPermissionRequiredMixin, TemplateView):
    permission_required = True
    template_name = None
    success_message = None
    model_name = None
    model = None
    title = None
    datatable_cols = None
    searchDB = True
    lenDB = True
    success_url = True
    datatableEnable = True
    datatableURL = None
    updateURL = None
    deleteURL = None
    deleteShow = True
    editShow = True
    api_url = None

    def get_api_url(self):
        if self.api_url:
            return self.api_url
        return get_model_api_url(self.model, self.__class__.__name__)

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        else:
            return str(self.model._meta).split('.')[1] + '/' + str(self.model._meta).split('.')[1] + '_list.html'

    def get_datatable_cols(self):
        return self.datatable_cols or self.model().get_datatable_columns()

    def get_success_url(self):
        return self.success_url or ""

    def get_deleteURL(self):
        return self.get_api_url()

    def get_updateURL(self):
        return self.updateURL or 'update/0'

    def get_datatableURL(self):
        return self.datatableURL or self.get_api_url() + 'datatable/'

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return self.get_model_name() + " " + _("Created Successfully")

    def get_model_name(self):
        if self.model_name:
            return self.model_name
        else:
            return self.model._meta.verbose_name

    def get_extra_context(self, context):
        # context['YOUR_DATA'] = ''
        return context

    def get_title(self):
        if self.title:
            return self.title
        elif self.model_name:
            return _("List") + " " + self.model_name
        return _("List") + " " + self.model._meta.verbose_name

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['model_name'] = self.get_model_name()
        context['api_url'] = self.get_api_url()
        if self.datatableEnable:
            context['datatableURL'] = self.get_datatableURL()
            context['cols'] = self.get_datatable_cols()
            context['searchDB'] = self.searchDB
            context['lenDB'] = self.lenDB
            context['deleteShow'] = self.deleteShow
            context['editShow'] = self.editShow
            context['deleteURL'] = self.get_deleteURL()
            context['editURL'] = self.get_updateURL()
        else:
            context['disableTable'] = True

        context = self.get_extra_context(context)
        return context


class DynamicCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CreateView):
    permission_required = True
    template_name = None
    api_url = None
    success_message = None
    model_name = None
    model = None
    title = None
    form = None
    datatable_cols = None
    searchDB = True
    lenDB = True
    form_fields = None
    form_fields_config = None
    datatableEnable = True
    datatableURL = None
    updateURL = None
    deleteURL = None
    deleteShow = True
    editShow = True
    is_admin_required = False

    def __init__(self, custom_model=None):
        super().__init__()
        if custom_model:
            self.model = custom_model

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        else:
            return str(self.model._meta).split('.')[1] + '/' + str(self.model._meta).split('.')[1] + '_create.html'

    def get_datatable_cols(self):
        return self.datatable_cols if self.datatable_cols else self.model().get_datatable_columns()

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        split = str(self.model._meta).replace('.', '/')
        return '/dashboard/' + split + '/create'

    def get_deleteURL(self):
        if self.deleteURL:
            return self.deleteURL
        return self.get_success_url().replace('create', 'delete/0')

    def get_api_url(self):
        if self.api_url:
            return self.api_url
        return get_model_api_url(self.model, self.__class__.__name__)

    def get_updateURL(self):
        if self.updateURL:
            return self.updateURL
        return self.get_success_url().replace('create', 'update/0')

    def get_datatableURL(self):
        return self.datatableURL if self.datatableURL else self.get_success_url().replace('/create', '/datatable')

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return self.get_model_name() + " " + _("Created Successfully")

    def get_form_fields_config(self):
        return self.form_fields_config

    def get_form_class(self):
        if self.form:
            return self.form
        if self.form_class:
            return self.form_class
        return dynamic_form(self.model, self.form_fields if self.form_fields else [], self.get_form_fields_config())

    def get_model_name(self):
        if self.model_name:
            return self.model_name
        else:
            return self.model._meta.verbose_name

    def get_extra_context(self, context):
        # context['YOUR_DATA'] = ''
        return context

    def get_title(self):
        if self.title:
            return self.title
        elif self.model_name:
            return 'افزودن ' + self.model_name
        return 'افزودن ' + self.model._meta.verbose_name

    def get_log(self, form):
        return log(self.request.user, 1, 3, True, form.instance)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['model_name'] = self.get_model_name()
        context['back'] = self.get_success_url()
        context['api_url'] = self.get_api_url()
        if self.datatableEnable:
            context['datatableURL'] = self.get_datatableURL()
            context['cols'] = self.get_datatable_cols()
            context['searchDB'] = self.searchDB
            context['lenDB'] = self.lenDB
            context['deleteShow'] = self.deleteShow
            context['editShow'] = self.editShow
            context['deleteURL'] = self.get_deleteURL()
            context['editURL'] = self.get_updateURL()
        else:
            context['disableTable'] = True

        context = self.get_extra_context(context)
        return context

    def form_valid(self, form):
        if DISABLE_FORM_SUBMIT:
            raise Http404()
        else:
            res = super().form_valid(form)
            self.get_log(form)
            messages.success(self.request, self.get_success_message())
            return res


class DynamicDatatableView(LoginRequiredMixin, CustomPermissionRequiredMixin, BaseDatatableView):
    model = None
    columns = None
    order_columns = None
    permission_required = None
    search_qs_field = 'title'

    def get_columns(self):
        return self.columns or self.model().get_datatable_columns()

    def get_order_columns(self):
        return self.order_columns or self.model().get_datatable_columns()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(**{self.search_qs_field + '__icontains': search}))
        return qs

    def render_column(self, row, column):
        colType = type(getattr(row, column)).__name__
        value = getattr(row, column)
        if value is None or colType == 'str' or colType == 'int':
            return super().render_column(row, column)

        if colType == 'datetime':
            return custom_change_date(value, mode=8) if value else ''
        if colType == 'date':
            return custom_change_date(value, mode=2) if value else ''

        if colType == 'bool':
            return 'bool-true' if value else 'bool-false'

        if colType == 'ManyRelatedManager':
            return ' - '.join([str(x) for x in getattr(row, column).all()])

        if colType == 'FieldFile':
            return value.url if value else 'file-null'

        return super().render_column(row, column)


class DynamicUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, UpdateView):
    permission_required = True
    model = None
    form = None
    template_name = None
    success_url = None
    success_message = None
    form_fields = None
    api_url = None
    model_name = None
    form_fields_config = None
    title = None
    is_admin_required = None

    def get_form_fields_config(self):
        return self.form_fields_config

    def get_form_class(self):
        if self.form:
            return self.form
        if self.form_class:
            return self.form_class
        return dynamic_form(self.model, self.form_fields if self.form_fields else [], self.get_form_fields_config())

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        else:
            return str(self.model._meta).split('.')[1] + '/' + str(self.model._meta).split('.')[1] + '_update.html'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        split = str(self.model._meta).replace('.', '/')
        return '/dashboard/' + split + '/create'

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return self.get_model_name() + " " + _("Updated Successfully")

    def get_model_name(self):
        if self.model_name:
            return self.model_name
        else:
            return self.model._meta.verbose_name

    def get_extra_context(self, context):
        # context['YOUR_DATA'] = ''
        return context

    def get_title(self):
        if self.title:
            return self.title
        elif self.model_name:
            return _("Update") + " " + self.object.__str__()
        return _("Update") + " " + self.object.__str__()

    def get_log(self, form):
        return log(self.request.user, 2, 4, True, form.instance)

    def get_api_url(self):
        if self.api_url:
            return self.api_url
        return get_model_api_url(self.model, self.__class__.__name__)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['model_name'] = self.get_model_name()
        context['back'] = self.get_success_url()
        context['api_url'] = self.get_api_url()
        context['successURL'] = self.get_success_url()
        context = self.get_extra_context(context)

        return context

    def form_valid(self, form):
        if DISABLE_FORM_SUBMIT:
            raise Http404()
        else:
            res = super().form_valid(form)
            self.get_log(form)
            messages.success(self.request, self.get_success_message())
            return res


class DynamicDeleteView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    model = None
    permission_required = True

    def get(self, request, pk):
        if DISABLE_FORM_SUBMIT:
            raise Http404()
        try:
            log(self.request.user, 3, 5, True, self.model.objects.get(pk=pk))
            self.before_delete()
            self.model.objects.get(pk=pk).delete()
            self.after_delete()
            return HttpResponse(status=200)
        except Exception as e:
            raise Http404

    def after_delete(self):
        pass

    def before_delete(self):
        pass


class SettingCreateView(DynamicCreateView):
    template_name = 'dynamic/create.html'

    def get_deleteURL(self):
        return '/api/v1/{0}/0'.format(str(self.model._meta).split('.')[1])

    def get_datatableURL(self):
        return '/api/v1/{0}/datatable/'.format(str(self.model._meta).split('.')[1])

    def get_createURL(self):
        return '/api/v1/{0}/'.format(str(self.model._meta).split('.')[1])

    def get_context_data(self, *args, **kwargs):
        res = super().get_context_data(*args, **kwargs)
        res['createURL'] = self.get_createURL()
        res['updateApiURL'] = self.get_createURL()
        return res


class SettingUpdateView(DynamicUpdateView):
    template_name = 'dynamic/update.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context_pk = self.kwargs['pk']
        context['context_pk'] = context_pk
        context['updateApiURL'] = '/api/v1/{0}/{1}/'.format(str(self.model._meta).split('.')[1], context_pk)
        context['successURL'] = self.get_success_url()
        return context
