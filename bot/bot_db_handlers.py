from bot.models import Category, Product, Cart, CartItem, TGUsers
from django.db.models import F
from asgiref.sync import sync_to_async

@sync_to_async
def start_user(id, username):
    user,created = TGUsers.objects.get_or_create(user_id = id)
    user.username = username
    user.save()
    Cart.objects.get_or_create(user=user)
    return user

@sync_to_async
def product_create(data):
    category = Category.objects.get(name=data['category'])
    product = Product.objects.create(
        title=data['title'],
        price=data['price'],
        category=category,
        image=data['image'],
    )
    product.save()
    return product

@sync_to_async
def product_detail(id):
    product = Product.objects.get(id = id)
    return product

@sync_to_async
def product_add_or_remove_to_cart(id, user_id, action):
    product = Product.objects.get(id = id)
    user = TGUsers.objects.get(user_id=user_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.update_or_create(product=product,cart=cart)
    if action=='add_one':
        cart_item.quantity = cart_item.quantity+1
    else:
        cart_item.quantity = (cart_item.quantity-1) if cart_item.quantity !=0 else cart_item.quantity
    cart_item.save()
    cart.total_price = cart_item.product.price * cart_item.quantity
    cart.save()
    return cart_item

@sync_to_async
def category_create_or_get(name):
    try:
        category = Category.objects.get(name = name)
        return category
    except:
        category = Category.objects.create(name = name).save()
        return category
    
@sync_to_async
def category_get_by_product(id):
    category = Product.objects.get(id=id).category
    return category

@sync_to_async
def cart_get(user_id):
    user = TGUsers.objects.get(user_id = user_id)
    cart = Cart.objects.get(user = user)
    cart_items = CartItem.objects.all().filter(quantity__gt = 0, cart = cart)
    text = f"✅✅✅ВАШ ЗАКАЗ✅✅✅\n\n{', '.join(' '.join((i.product.title, '-',str(i.quantity))) for i in cart_items)}\n\nСумма: {cart.total_price} сом"
    return text