from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Displays stats related to Article and Comment models'

    def add_arguments(self, parser):
        parser.add_argument('-username', '--username', type=str, help='Username of superuser')
        parser.add_argument('-password', '--password', type=str, help='Password of superuser')
        parser.add_argument('-email', '--email', type=str, help='Email of superuser')
        parser.add_argument('-fname', '--fname', type=str, help='First Name of superuser')
        parser.add_argument('-lname', '--lname', type=str, help='Last Name of superuser')

    def handle(self, *args, **kwargs):
        username = kwargs.get('username') or "mamad"
        password = kwargs.get('password') or "mamad"
        email = kwargs.get('email') or "mamad@mail.com"
        first_name = kwargs.get('fname') or "mohammad"
        last_name = kwargs.get('lname') or "shekari"
        if User.objects.filter(username=username).first():
            raise ValueError(f"This Username ({username}) already taken")
        if User.objects.filter(email=email).first():
            raise ValueError(f"This Email ({email}) already taken")
        User(
            username=username,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=True,
        ).save()
        print(f'Superuser ({username}) created successfully!')
