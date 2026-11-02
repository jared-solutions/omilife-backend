from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@omilife.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Admin user created successfully. Username: admin, Password: admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )