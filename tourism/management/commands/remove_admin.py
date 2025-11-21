from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Remove admin privileges from a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to remove admin from')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully removed admin privileges from "{username}"!')
            )
            self.stdout.write(f'User: {user.first_name} {user.last_name}')
            self.stdout.write(f'Email: {user.email}')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist!')
            )
            self.stdout.write('Available users:')
            for user in User.objects.all():
                role = "Admin" if user.is_staff else "User"
                self.stdout.write(f'  - {user.username} ({role})')