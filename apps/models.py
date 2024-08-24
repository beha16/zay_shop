from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django_resized import ResizedImageField


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    image = models.ImageField(upload_to='user/', null=True, blank=True, default='user/user_image.png')


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField()
    colors = models.CharField(max_length=255)
    specification = models.TextField()
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    top_seller = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        ordering = ['-created_at']

    @property
    def is_new(self):
        return now() - timedelta(days=7) < self.created_at

    def __str__(self) -> str:
        return self.name


class ProductImage(BaseModel):
    image = ResizedImageField(size=[800, 800], upload_to='product/', crop=['middle', 'center'],  blank=True, null=True)
    # image = models.ImageField(upload_to='product/', null=True, blank=True, default=)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return self.product.name


class Order(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self) -> str:
        return self.product.name


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def is_stock(self):
        return self.product.quantity > 0

    def __str__(self) -> str:
        return self.product.name


class Basket(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def is_stock(self):
        return self.product.quantity > 0



    def __str__(self) -> str:
        return self.product.name