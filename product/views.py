from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Order, Cart, Color, Size, Brand, Review, Category
from .forms import ProductCreationForm
from .filters import ProductFilter
from django.db import models
from django.core.paginator import Paginator



def index_view(request):
    products = Product.objects.filter(is_active=True)

    top_categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('-product_count')[:3]

    top_brands = Brand.objects.annotate(
        product_count=Count('products')
    ).order_by('-product_count')[:3]


    for product in products:
        reviews = Review.objects.filter(product=product)
        if reviews.exists():
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            product.average_rating = round(avg_rating, 1)
        else:
            product.average_rating = 0

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mainPages/index.html', context={
        'products': page_obj,
        'top_categories': top_categories,
        'top_brands': top_brands,
        'page_obj': page_obj
    })


def detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product_id)


    if reviews.exists():
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        product.average_rating = round(avg_rating, 1)
    else:
        product.average_rating = 0

    return render(request, 'mainPages/detail.html', context={'product': product, 'reviews': reviews})

@require_POST
def add_to_cart_view(request, product_id):

    color_id = request.POST.get('color_id')
    size_id = request.POST.get('size_id')
    quantity = int(request.POST.get('quantity', 1))

    if not all([color_id, size_id]):
        messages.error(request, "Choose color and size!")
        return redirect('detail_view', product_id=product_id)


    product = get_object_or_404(Product, id=product_id)
    color = get_object_or_404(Color, id=color_id)
    size = get_object_or_404(Size, id=size_id)


    cart, created = Cart.objects.get_or_create(user=request.user)


    existing_order = Order.objects.filter(
        user=request.user,
        product=product,
        color=color,
        size=size,
        carts=cart
    ).first()

    if existing_order:

        existing_order.quantity += quantity
        existing_order.save()
    else:

        order = Order.objects.create(
            user=request.user,
            product=product,
            color=color,
            size=size,
            quantity=quantity
        )

        cart.orders.add(order)
        messages.success(request, "Product added to cart!")
    return redirect('index_view')


def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    total_price = 0

    if cart:
        orders = cart.orders.all()
        for order in orders:
            total_price += order.product.price * order.quantity

        cart.total = total_price
        cart.save()
    else:

        cart = Cart.objects.create(user=user)

    return render(request, 'mainPages/cart.html', context={
        'cart': cart,
        'total_price': total_price
    })


def cart_remove_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart = Cart.objects.filter(user=request.user).first()
    cart.orders.remove(order)
    messages.success(request, "Product removed from cart!")
    return redirect('cart_view')



def create_product_view(request):
    form = ProductCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        form.save_m2m()

        # Restore copying available_colors to product.color
        product.color.set(product.available_colors.all())

        messages.success(request, "Product created successfully!")
        return redirect('index_view')

    brands = Brand.objects.all()
    colors = Color.objects.all()
    return render(request, 'mainPages/create_product.html', {
        'form': form,
        'brands': brands,
        'colors': colors
    })

def user_products_view(request):
    products = Product.objects.filter(user=request.user, is_active=True)

    # Restore syncing between available_colors and color
    for product in products:
        product.color.set(product.available_colors.all())

    return render(request, 'mainPages/user_products.html', context={'products': products})

def user_product_deactivation(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = False
    product.save()
    messages.success(request, "Product deactivated successfully!")
    return redirect('user_products')


def user_product_deletion(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('user_products')


def user_product_activation(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not product.is_active:
        product.is_active = True
        product.save()
    messages.success(request, "Product activated successfully!")
    return redirect('user_products')

def user_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    form = ProductCreationForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        product = form.save(commit=False)
        product.save()
        form.save_m2m()

        # Restore syncing between available_colors and color
        product.color.set(product.available_colors.all())

        messages.success(request, "Product updated successfully!")
        return redirect('user_products')


    if not request.POST:  # Only set initial data on GET request
        form.initial['brand_name'] = product.brand.name

    brands = Brand.objects.all()
    colors = Color.objects.all()
    return render(request, 'mainPages/edit_product.html', {
        'form': form,
        'product': product,
        'brands': brands,
        'colors': colors
    })


def product_list(request):
    filter = ProductFilter(request.GET, queryset=Product.objects.filter(is_active=True))

    # Check if it's an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    return render(request, 'mainPages/index.html', {
        'filter': filter,
        'products': filter.qs,
        'is_ajax': is_ajax
    })

def filtered_products(request):
    products = Product.objects.filter(is_active=True)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    filter = ProductFilter(request.GET, queryset=Product.objects.filter(is_active=True))
    return render(request, 'mainPages/filtered_products.html', {'filter': filter, products: products})


def send_review(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)

        existing_review = Review.objects.filter(product=product, user=request.user).first()

        if existing_review:

            existing_review.rating = request.POST.get('rating')
            existing_review.comment = request.POST.get('review_text')
            existing_review.save()
            messages.success(request, 'Review updated successfully!')
        else:

            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=request.POST.get('rating'),
                comment=request.POST.get('review_text')
            )
            review.save()
            messages.success(request, 'Review submitted successfully!')

    return redirect('detail_view', product_id=product_id)


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product_id = review.product.id  # Store the product_id before deleting the review
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('detail_view', product_id=product_id)


def top_up_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            if amount < 5:
                messages.error(request, "Minimum top-up amount is $5.")
                return redirect('top_up')
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid amount.")
            return redirect('top_up')


        card_details = {
            'card_number': request.POST.get('card_number'),
            'expiry': request.POST.get('expiry'),
            'cvv': request.POST.get('cvv'),
            'cardholder': request.POST.get('cardholder')
        }


        if not all(card_details.values()):
            messages.error(request, "Please fill in all card details.")
            return redirect('top_up')


        messages.success(request, f"Balance successfully topped-up to ${amount:.2f}.")


        user = request.user
        user.balance += amount
        user.save()

        return redirect('index_view')

    return render(request, 'top_up/top_up_main.html')


def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if user.balance < cart.total:
        messages.error(request, "Insufficient balance!")
        return redirect('cart_view')
    else:
        user.balance -= cart.total
        user.save()
        cart.delete()
        messages.success(request, "Checkout successful!")
        return redirect('index_view')
