from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=50
    )

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    price = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Фото продукта',
        blank=True,
        null=True,
        upload_to='images/'
    )
    

    def __str__(self):
        return f"{self.title} - {self.price}"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Cart(models.Model):
    user_id = models.PositiveSmallIntegerField(unique=True)
    total_price = models.PositiveIntegerField()
    user_name = models.CharField(
        max_length=255
    )

class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField()