from django.apps import apps
from django.contrib import admin

for key, model in apps.get_app_config('badi_blog').models.items():
    admin.site.register(model)
