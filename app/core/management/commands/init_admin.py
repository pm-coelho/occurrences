from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Creates and admin user if it doesn't exist

    ps: this is a bad practice if it is used in any file checked on vcs
        I'm using this method because it is the easiest to setup
        and test with the postman collection
    """

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                'Admin created: {} ({}) : {}'.format(username, email, password)
            )
        else:
            self.stdout.write('No need to create admin user.')
