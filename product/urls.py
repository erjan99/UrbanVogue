from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index_view, name='index_view'),
    path('detail_view/<int:product_id>/', detail_view, name='detail_view'),
    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)