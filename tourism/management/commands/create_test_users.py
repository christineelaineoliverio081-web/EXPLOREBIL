from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create test admin and regular user accounts'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@explorebiliran.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create regular user
        if not User.objects.filter(username='user').exists():
            user = User.objects.create_user(
                username='user',
                email='user@explorebiliran.com',
                password='user123',
                first_name='Regular',
                last_name='User',
                is_staff=False,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS('Regular user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Regular user already exists'))

        self.stdout.write(self.style.SUCCESS('\n=== TEST ACCOUNTS ==='))
        self.stdout.write(self.style.SUCCESS('ADMIN ACCOUNT:'))
        self.stdout.write(self.style.SUCCESS('Username: admin'))
        self.stdout.write(self.style.SUCCESS('Email: admin@explorebiliran.com'))
        self.stdout.write(self.style.SUCCESS('Password: admin123'))
        self.stdout.write(self.style.SUCCESS('\nREGULAR USER ACCOUNT:'))
        self.stdout.write(self.style.SUCCESS('Username: user'))
        self.stdout.write(self.style.SUCCESS('Email: user@explorebiliran.com'))
        self.stdout.write(self.style.SUCCESS('Password: user123'))