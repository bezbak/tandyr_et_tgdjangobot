from django.contrib import admin
from .models import Cart, CartItem, Product,Category, TGUsers
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(TGUsers)
admin.site.register(Category)