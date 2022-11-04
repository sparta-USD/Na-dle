from django.core.management.base import BaseCommand
from users.models import User
from django_seed import Seed
from django.contrib.auth.hashers import make_password
import random
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many users do you want to create?",
        )
    
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "password" : make_password("1234"),
                "is_admin" : False
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
        
    # python manage.py create-users --number 50
    # => 임의의 유저 50명 생성함