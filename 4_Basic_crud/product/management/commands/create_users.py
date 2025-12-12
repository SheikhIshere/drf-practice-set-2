from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import uuid
import random

User = get_user_model()


def make_random_pp():
    return f'@password_{random.randint(1000,9999)}'

class Command(BaseCommand):
    help = 'Create sample users with Bangladeshi names and emails'

    def handle(self, *args, **options):
        bangladeshi_first_names = [
            "Rahim",
            "Karim",
            "Hossain",
            "Sultana",            
            "Faruk",
            "Aziz",
            "Hasan",
            "Rana"
        ]
        bangladeshi_surnames = [
            "Chowdhury",
            "Hossain",
            "Islam",            
            "Ahmed",
            "Khan",
            "Sheikh",            
            "Chowdhury",
        ]

        email_domains = ["gmail.com", "yahoo.com", "hotmail.com"]

        for _ in range(100):  # Create 10 users
            username = f"user_{uuid.uuid4().hex[:8]}"
            first_name = random.choice(bangladeshi_first_names)
            last_name = random.choice(bangladeshi_surnames)
            email_domain = random.choice(email_domains)
            email = f"{first_name}{random.randint(666,9999)}{last_name}{random.randint(100,999)}@{email_domain}"
            password = make_random_pp()
            # Create the user with a random password
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            self.stdout.write(self.style.SUCCESS(f"Created user: {username} with email: {email} and password: {password}"))

        self.stdout.write(self.style.SUCCESS("Users created successfully!"))
