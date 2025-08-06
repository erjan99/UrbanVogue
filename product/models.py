from django.contrib.auth import get_user_model
from django.db import models
from .choices import GenderChoices


user_model = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='media/categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=300, unique=True)
    logo = models.ImageField(upload_to='media/brands/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code



COLOR_MAP = {
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#00FF00",
    "white": "#FFFFFF",
    "black": "#000000",
    "yellow": "#FFFF00",
    # add more as needed
}

class Color(models.Model):
    color = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7, default="#000000")

    def save(self, *args, **kwargs):
        name = self.color.strip().lower()
        if name in COLOR_MAP:
            self.hex_code = COLOR_MAP[name]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.color


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Product details
    stock_quantity = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GenderChoices, default='U')
    available_sizes = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color)

    # Images
    main_image = models.ImageField(upload_to='media/products/')
    created_at = models.DateTimeField(auto_now_add=True)

    # Status
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_available_sizes_list(self):
        return [size.code for size in self.available_sizes.all()]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/products/gallery/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image"


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.rating} stars by {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  # Changed from CharField to ForeignKey
    quantity = models.PositiveIntegerField(default=1)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)  # Changed from CharField to ForeignKey
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Added timestamp

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class Cart(models.Model):
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name='carts', blank=True)  # Changed to ManyToMany

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_items(self):
        return sum(order.quantity for order in self.orders.all())

    @property
    def total_price(self):
        return sum(order.product.price * order.quantity for order in self.orders.all())

