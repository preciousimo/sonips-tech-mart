from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from product.models import Product, Wishlist

def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user)
        context = {
            'wishlist_items': wishlist_items
        }
        return render(request, 'wishlist/wishlist.html', context)
    else:
        messages.error(request, 'Please log in to view your wishlist.')
        return redirect('login')

def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.create(user=user, product=product)
        messages.success(request, 'Product added to wishlist successfully.')
        return redirect('wishlist')
    else:
        messages.error(request, 'Please log in to add items to your wishlist.')
        return redirect('login')

def remove_from_wishlist(request, item_id):
    if request.user.is_authenticated:
        try:
            wishlist_item = Wishlist.objects.get(id=item_id, user=request.user)
            wishlist_item.delete()
            messages.success(request, 'Product removed from wishlist successfully.')
        except Wishlist.DoesNotExist:
            messages.error(request, 'Wishlist item does not exist.')
        return redirect('wishlist')
    else:
        messages.error(request, 'Please log in to remove items from your wishlist.')
        return redirect('login')