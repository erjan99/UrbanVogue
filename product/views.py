from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Order, Cart, Color, Size



def index_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'mainPages/index.html', context={'products': products})

def detail_view(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    return render(request, 'mainPages/detail.html', context={'product': product})


@require_POST
def add_to_cart_view(request, product_id):
    # Get form data
    color_id = request.POST.get('color_id')
    size_id = request.POST.get('size_id')
    quantity = int(request.POST.get('quantity', 1))

    # Validate inputs
    if not all([color_id, size_id]):
        messages.error(request, "Пожалуйста, выберите цвет и размер")
        return redirect('product_detail', pk=product_id)

    # Get objects
    product = get_object_or_404(Product, id=product_id)
    color = get_object_or_404(Color, id=color_id)
    size = get_object_or_404(Size, id=size_id)

    # Create Order
    order = Order.objects.create(
        user=request.user,
        product=product,
        color=color,  # Now using a ForeignKey
        size=size,    # Now using a ForeignKey
        quantity=quantity
    )

    # Add to user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.orders.add(order)

    messages.success(request, "Товар добавлен в корзину")
    return redirect('cart')  # Redirect to cart page

def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    return render(request, 'mainPages/cart.html', context={'cart': cart})


