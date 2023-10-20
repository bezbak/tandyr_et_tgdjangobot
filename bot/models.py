from django.db import models

# Create your models here.

class TGUsers(models.Model):
    user_id = models.PositiveSmallIntegerField(unique=True)
    username = models.CharField(
        max_length=255,
        null=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    
    def __str__(self):
        return f"{self.id} - @{self.username}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
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
    image = models.CharField(
        'Фото продукта',
        max_length=555
    )
    

    def __str__(self):
        return f"{self.title} - {self.price}"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Cart(models.Model):
    total_price = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        TGUsers,
        related_name='carts',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.total_price}"
    
    class Meta:
        verbose_name = 'Корзинка'
        verbose_name_plural = 'Корзинки'

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
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"
    
    class Meta:
        verbose_name = 'Продукт корзинки'
        verbose_name_plural = 'Продукты  корзинки'