from tkinter.font import names

from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index_view, name='index_view'),
    path('detail_view/<int:product_id>/', detail_view, name='detail_view'),

    # Cart
    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart_view/', cart_view, name='cart_view'),
    path('cart_remove_product/<int:order_id>/', cart_remove_view, name='cart_remove_product'),
    path('cart_checkout/', checkout, name='checkout'),

    # Product
    path('create_product/', create_product_view, name='create_product'),
    path('user_products/', user_products_view, name='user_products'),
    path('user_product_deactivation/<int:product_id>/', user_product_deactivation, name='user_product_deactivation'),
    path('user_product_activation/<int:product_id>/', user_product_activation, name='user_product_activation'),
    path('user_product_delete/<int:product_id>/', user_product_deletion, name='user_product_deletion'),
    path('user_product_edit/<int:product_id>/', user_product_edit, name='user_product_edit'),

    # Filters
    path('products/', product_list, name='product_list'),
    path('filtered_products', filtered_products, name='filtered_products'),

    # Review
    path('send_review/<int:product_id>/', send_review, name='send_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),

    # Top Up
    path('top_up/', top_up_view, name='top_up_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)