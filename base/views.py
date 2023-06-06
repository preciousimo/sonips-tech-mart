from django.http import HttpResponse
from django.shortcuts import render

from product.models import Product, Category

def index(request):
    products = Product.objects.all()

    context = {
        "products":products
    }
    return render(request, 'index.html', context)