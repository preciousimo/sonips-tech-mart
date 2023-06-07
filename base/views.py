from django.http import HttpResponse
from django.shortcuts import render

from product.models import Product, Category
import random

def index(request):
    products = list(Product.objects.all())
    total_products = len(products)
    num_products = min(total_products, 4)
    products = random.sample(products, num_products)

    context = {
        "products":products
    }
    return render(request, 'index.html', context)