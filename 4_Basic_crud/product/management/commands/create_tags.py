# product/management/commands/create_tags.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from product.models import Tag
from django.db import transaction
import random
import itertools

User = get_user_model()

TAG_BASES = [
    "Featured","New Arrival","On Sale","Bestseller","Limited",
    "Organic","Imported","Local","Hot Pick","Clearance",
    "Editor's Choice","Premium","Budget","Eco Friendly","Seasonal",
    "Trending","Top Rated","Exclusive","Bundle","Refurbished",
    "Warranty","Fast Shipping","Handmade","Gift","Popular",
    "Durable","Lightweight","Compact","Portable","Luxury",
    "Family Pack","Single Pack","Limited Edition","Refill","Sample",
    "Recommended","Verified","Authentic","Certified","Wholesale",
    "Retail","Outlet","Discounted","Promo","Clearance",
    "Eco","Recycled","New","Classic","Vintage"
]

def title_candidates():
    # generate many name variants by combining bases with adjective/number
    adjectives = ["Prime","Plus","Max","Pro","Ultra","Smart","Active","Safe","Fresh","Pure"]
    pool = []
    for base in TAG_BASES:
        pool.append(base)
        for adj in adjectives[:4]:
            pool.append(f"{adj} {base}")
    random.shuffle(pool)
    for name in pool:
        yield name

class Command(BaseCommand):
    help = "Create sample tags and unique slugs; assigns tags to existing users"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=30, help='How many tags to create')

    def handle(self, *args, **options):
        count = options['count']
        users = list(User.objects.all())
        if not users:
            admin, _ = User.objects.get_or_create(
                email="admin@example.com",
                defaults={"username": "admin", "is_active": True}
            )
            users = [admin]

        existing = set(Tag.objects.values_list('title', flat=True))
        created = []
        cand = title_candidates()
        user_cycle = itertools.cycle(users)
        attempts = 0
        max_attempts = count * 10

        with transaction.atomic():
            while len(created) < count and attempts < max_attempts:
                attempts += 1
                try:
                    title = next(cand)
                except StopIteration:
                    title = f"Tag{random.randint(1000,99999)}"
                if title in existing:
                    continue
                owner = next(user_cycle)
                tag_obj, flag = Tag.objects.get_or_create(title=title, defaults={'user': owner})
                if flag:
                    created.append((tag_obj.title, owner.email))
                    existing.add(tag_obj.title)

        for t, owner in created:
            self.stdout.write(self.style.SUCCESS(f"Created tag: '{t}' (user: {owner})"))

        if len(created) < count:
            self.stdout.write(self.style.WARNING(f"Created {len(created)} tags (requested {count})."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Created {len(created)} tags successfully."))
