from django.shortcuts import render
from .models import *


def index_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'mainPages/index.html', context={'products': products})
