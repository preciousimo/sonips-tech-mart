from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist, name='wishlist'),

    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
]
