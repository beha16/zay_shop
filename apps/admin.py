from django.contrib import admin
from .models import User, Product, ProductImage, Order, Wishlist, Category, Basket

# Register your models here.


# admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'top_seller')
    list_filter = ('name', 'price', 'top_seller')
    inlines = [ProductImageAdmin, ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'email')



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user', 'product')



@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')
    list_filter = ('user', 'product')