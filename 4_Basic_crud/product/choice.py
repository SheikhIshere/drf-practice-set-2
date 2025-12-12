"""
choice
"""

from django.db import models

class TYPE(models.IntegerChoices):
    ELECTRONICS = 1, "Electronics"
    CLOTHING = 2, "Clothing"
    FOOD = 3, "Food & Beverages"
    FURNITURE = 4, "Furniture"
    BEAUTY_PERSONAL_CARE = 5, "Beauty & Personal Care"
