from .models import Product
import django_filters

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Product Name')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Price greater than')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Price less than')

    class Meta:
        model = Product
        fields = {
            'brand': ['exact'],
            'category': ['exact'],
            'gender': ['exact'],
        }