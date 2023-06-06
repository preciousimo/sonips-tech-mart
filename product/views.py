from django.http import HttpResponse
from django.shortcuts import render

from product.models import Product, Category

def product_list(request):
    products = Product.objects.all()

    context = {
        "products":products
    }
    return render(request, 'product/product-list.html', context)