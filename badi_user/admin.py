from django.apps import apps
from django.contrib import admin

for key, model in apps.get_app_config('user').models.items():
    admin.site.register(model)
