from django.conf import settings
from django.db import models

# ------------------ Choices ------------------
SIZE_CHOICES = [
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

# ------------------ Models ------------------

class ClothesGender(models.Model):
    name = models.CharField(max_length=255, verbose_name="Gender")

    class Meta:
        verbose_name = "Clothes Gender"
        verbose_name_plural = "Clothes Genders"

    def __str__(self):
        return self.name


class ClothesAge(models.Model):
    name = models.CharField(max_length=255, verbose_name="Age Group")

    class Meta:
        verbose_name = "Clothes Age"
        verbose_name_plural = "Clothes Ages"

    def __str__(self):
        return self.name


class ClothesBrand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Brand Name")

    class Meta:
        verbose_name = "Clothes Brand"
        verbose_name_plural = "Clothes Brands"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Price")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='media/product_images/', verbose_name="Image")
    clothes_age = models.ForeignKey(ClothesAge, on_delete=models.CASCADE, verbose_name="Age Group")
    clothes_gender = models.ForeignKey(ClothesGender, on_delete=models.CASCADE, verbose_name="Gender")
    brand = models.ForeignKey(ClothesBrand, on_delete=models.CASCADE, verbose_name="Brand")
    product_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, verbose_name="Size")
    color = models.CharField(max_length=255, verbose_name="Color")
    material = models.CharField(max_length=255, verbose_name="Material")
    stock = models.PositiveIntegerField(verbose_name="Stock Quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        unique_together = ('product', 'size', 'color', 'material')

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Product")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    review_text = models.TextField(verbose_name="Review")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name="Product Variant")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('user', 'product_variant')

    def __str__(self):
        return f"{self.user.username} - {self.product_variant} x {self.quantity}"
