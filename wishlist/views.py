from django.http import HttpResponse
from django.shortcuts import redirect, render

from product.models import Product, Wishlist

# Create your views here.
def wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist/wishlist.html', context)

def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.create(user=user, product=product)
        # You can add any additional logic here (e.g., showing a success message)
        return redirect('wishlist')
    else:
        # Handle the case where the user is not authenticated
        return redirect('login')

def remove_from_wishlist(request, item_id):
    # Retrieve the Wishlist object using the item_id
    try:
        wishlist_item = Wishlist.objects.get(id=item_id)
    except Wishlist.DoesNotExist:
        # Handle the case when the wishlist item is not found
        # Redirect or show an error message
        return HttpResponse("Wishlist item does not exist.")
    
    # Delete the wishlist item
    wishlist_item.delete()

    # Redirect to the wishlist page or any other desired location
    return redirect('wishlist') 
