from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Avg, FloatField
from django.db.models.functions import Cast

from product.models import Product, Category, ProductReview
from .forms import ProductReviewForm

import random

def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.exclude(title='Phones')
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
    return render(request, 'product/product_list.html', context)


def product_detail(request, pid):
    product = Product.objects.get(pid=pid)

    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    total_products = len(products)
    num_products = min(total_products, 4)
    productss = random.sample(list(products), num_products)

    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg(Cast('rating', output_field=FloatField())))

    review_form = ProductReviewForm()
    p_image = product.p_images.all()

    context = {
        "product": product,
        "review_form": review_form,
        "reviews": reviews,
        "average_rating": average_rating,
        "p_image": p_image,
        "products": productss,
    }

    return render(request, "product/product_detail.html", context)
