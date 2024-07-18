import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badi_users_project.settings')

application = get_wsgi_application()
User = get_user_model()
if __name__ == '__main__':
    user = User(
        username="test_superuser",
        email="info@badidesign.ir",
        password="test_superuser",
        is_superuser=True,
    )
    user.save()
