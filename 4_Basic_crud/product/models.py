"""
Docstring for product.models
"""

"""
planing:

1: BaseModel:(models.Model)
    created_at        (datetime)
    updated_at        (datetime)

    class meta:
        abs true

        
2:Tag:(BaseModel)
    id
    title
    

3: Product:(BaseModel)
    id              pk / uuid
    name            char
    price           float
    type            choice
    brand           char
    description     text
    stock_quantity  int
    image           img
    tag             m2m
    is_returnable   bool
    
"""


# core imports
from django.db import models
from django.utils import timezone
from uuid import uuid4
from django.utils.text import slugify


# user import
from django.contrib.auth import get_user_model
User = get_user_model()

# choice import
from .choice import TYPE


"""
base Model
"""
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



""" 
tag
"""
class Tag(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def __str__(self):
        return self.title

    def _generate_unique_slug(self, base):
        slug = slugify(base)[:60].rstrip('-')
        candidate = slug
        counter = 1
        while Tag.objects.filter(slug=candidate).exists():
            candidate = f"{slug[:56]}-{counter}"
            counter += 1
        return candidate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug(self.title)
        super().save(*args, **kwargs)

""" 
Brand
"""
class Brand(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title        


"""
product
"""
class Product(BaseModel):
    # pk / fk
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # general description
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='product/image/', blank=True)
    stock_quantity = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    
    # classification
    type = models.IntegerField(choices=TYPE.choices, default=TYPE.ELECTRONICS)    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    
    # policy
    is_returnable = models.BooleanField(default=False)
    return_day = models.PositiveIntegerField(
        blank=True, 
        null=True,
        default=0
    )
    warrantee_availability = models.BooleanField(default=False)
    warranty_period = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Period in days"
    )

    def __str__(self):
        return self.title        

