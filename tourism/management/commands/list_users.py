from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'List all users and their roles'

    def handle(self, *args, **options):
        users = User.objects.all().order_by('username')
        
        if not users:
            self.stdout.write(self.style.WARNING('No users found!'))
            return
            
        self.stdout.write(self.style.SUCCESS('\n=== ALL USERS ==='))
        self.stdout.write(f'{"Username":<15} {"Name":<20} {"Email":<25} {"Role":<10}')
        self.stdout.write('-' * 70)
        
        for user in users:
            role = "Admin" if user.is_staff else "User"
            name = f"{user.first_name} {user.last_name}".strip() or "No name"
            
            self.stdout.write(
                f'{user.username:<15} {name:<20} {user.email:<25} {role:<10}'
            )
            
        self.stdout.write(f'\nTotal users: {users.count()}')