# product/management/commands/create_brands.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from product.models import Brand
import random
import itertools

User = get_user_model()

PREFIXES = [
    "Basundhara","Pran","Meghna","Rupsha","Sonar","Bangla","Deshi","Nirapod",
    "Shanto","Sundar","Green","Royal","Sky","Metro","Aarong","Dhaka","Sylhet",
    "Chattogram","Padma","Jamuna","Bongo","Nodi","Noor","Nirman","Shakti"
]

SUFFIXES = [
    "Foods","Enterprises","Exports","Supplies","Industries","Fashions","Mart",
    "Collections","Trading","Works","Creations","Beverages","Electronics",
    "Textiles","Auto","Home","Care","Pharma","Agro","Logistics","Solutions",
    "Style","Bazaar","Studio"
]

def generate_candidate_names():
    """Yield many candidate brand names (prefix + suffix) in random order."""
    combos = [f"{p} {s}" for p, s in itertools.product(PREFIXES, SUFFIXES)]
    random.shuffle(combos)
    for name in combos:
        yield name

class Command(BaseCommand):
    help = "Create 100 unique Bangladeshi brand names and attach them to users"

    def handle(self, *args, **options):
        # Collect users to assign brands to
        users = list(User.objects.all())
        if not users:
            # Create a fallback admin user if DB is empty
            admin, _ = User.objects.get_or_create(
                email="admin@example.com",
                defaults={"username": "admin", "is_active": True}
            )
            users = [admin]

        existing_titles = set(
            Brand.objects.values_list('title', flat=True)
        )

        created = []
        candidate_iter = generate_candidate_names()
        attempts = 0
        max_attempts = 10000  # safety net

        user_cycle = itertools.cycle(users)

        with transaction.atomic():
            while len(created) < 100 and attempts < max_attempts:
                attempts += 1
                try:
                    base_name = next(candidate_iter)
                except StopIteration:
                    # fallback: create a new random synthetic name
                    base_name = f"Brand{random.randint(1000,99999)}"

                name = base_name.strip()
                # Ensure uniqueness in-memory + DB
                if name in existing_titles:
                    # try adding a numeric suffix to make unique
                    suffix_try = 1
                    new_name = f"{name} {suffix_try}"
                    while new_name in existing_titles:
                        suffix_try += 1
                        new_name = f"{name} {suffix_try}"
                    name = new_name

                # final safety: truncate to 50 chars (model limit)
                if len(name) > 50:
                    name = name[:50].strip()

                # still double-check
                if name in existing_titles:
                    continue

                owner = next(user_cycle)
                brand_obj, created_flag = Brand.objects.get_or_create(
                    title=name,
                    defaults={"user": owner}
                )
                if created_flag:
                    existing_titles.add(name)
                    created.append((brand_obj.title, owner.email))
                # if not created (already existed) we just skip

            # end while

        # Output summary
        for title, owner_email in created:
            self.stdout.write(self.style.SUCCESS(f"Created Brand: '{title}' (owner: {owner_email})"))

        if len(created) < 100:
            self.stdout.write(self.style.WARNING(
                f"Only created {len(created)} unique brands. "
                "Either DB already had many of the generated names or candidate pool exhausted."
            ))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully created 100 unique brands."))
