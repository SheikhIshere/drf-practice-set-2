# products/management/commands/create_products.py
from django.core.management.base import BaseCommand
from product.models import Product, Brand, Tag
from account.models import Account
import random
from uuid import uuid4

class Command(BaseCommand):
    help = "Create dummy products"

    PRODUCT_NAMES = [
        "UltraPhone", "SmartWatch", "EcoBag", "Organic Shampoo", "Running Shoes",
        "Leather Wallet", "Desk Lamp", "Bluetooth Speaker", "Laptop Sleeve",
        "Travel Backpack", "Gaming Mouse", "Wireless Earbuds"
    ]

    DESCRIPTIONS = [
        "High quality and durable product.",
        "Best seller in its category.",
        "Limited edition, grab it fast.",
        "Top rated by customers.",
        "Eco-friendly and sustainable product."
    ]

    def handle(self, *args, **kwargs):
        users = list(Account.objects.filter(is_active=True))
        brands = list(Brand.objects.all())
        tags = list(Tag.objects.all())

        if not users or not brands or not tags:
            self.stdout.write(self.style.ERROR("Users, brands, or tags are missing!"))
            return

        products_created = 0
        for i in range(1000):  # create 100 products
            # Generate product name
            product_name = random.choice(self.PRODUCT_NAMES) + f" {random.randint(100,999)}"
            
            # Get random brand and its user
            brand = random.choice(brands)
            
            # FIX: Use brand.user NOT brand.owner
            product_owner = brand.user  # This is correct - matches your Brand model
            
            price = round(random.uniform(50, 1000), 2)
            stock = random.randint(10, 500)
            description = random.choice(self.DESCRIPTIONS)
            product_tags = random.sample(tags, k=min(3, len(tags)))

            # Create product - NOTE: Your model has 'title' not 'name'
            product = Product.objects.create(
                id=uuid4(),
                title=product_name,  # Changed from 'name' to 'title'
                brand=brand,
                user=product_owner,  # Using brand's user
                price=price,
                stock_quantity=stock,  # Changed from 'stock' to 'stock_quantity'
                description=description,
                type=random.randint(1, 5)  # Assuming TYPE has 5 choices
            )

            # Add tags
            product.tag.add(*product_tags)
            products_created += 1
            self.stdout.write(self.style.SUCCESS(f"Created product: {product_name}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {products_created} products."))