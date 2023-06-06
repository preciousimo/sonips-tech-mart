from django.http import HttpResponse
from django.shortcuts import render

from product.models import Product, Category

import random

def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    active_category = None
    
    if category_id:
        products = Product.objects.filter(category__id=category_id)
        active_category = Category.objects.get(id=category_id)
    else:
        products = list(Product.objects.all())
        total_products = len(products)
        num_products = min(total_products, 6)
        products = random.sample(products, num_products)
    
    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'product/product-list.html', context)
