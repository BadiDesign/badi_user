from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm

from badi_utils.dynamic import dynamic_form
from django.contrib.auth import get_user_model

User = get_user_model()


def user_form(fields=None, update=False):
    form_config = dynamic_form(model_class=User, just_data=True, get_fields=fields)

    class ModelFormCreator(ModelForm):
        class Meta:
            model = form_config.get('model')
            fields = form_config.get('fields')
            error_messages = form_config.get('error_messages')

        def __init__(self, *args, **kwargs):
            super(ModelFormCreator, self).__init__(*args, **kwargs)

            for key, field in enumerate(form_config.get('field_names')):
                self.fields[field].label = form_config.get('labels')[key]
                self.fields[field].required = form_config.get('required')[key]
                self.fields[field].widget.attrs = form_config.get('classes')[key]
                self.fields[field].widget.attrs['placeholder'] = form_config.get('labels')[key] + ' را وارد کنید ...'

        def clean_password(self):
            return make_password(self.cleaned_data['password'])

    return ModelFormCreator
