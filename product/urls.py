from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.product_list, name="product_list"),
    path('product/<pid>/', views.product_detail, name="product-detail"),

	path('search/', views.search_view, name="search"),
	
	path('cart/', views.cart, name="cart"),
    path('add-to-cart/', views.add_to_cart, name="add_to_cart"),
    path('update-cart/', views.update_cart, name="update-cart"),
    path('delete-from-cart/', views.delete_from_cart, name="delete-from-cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('process-order/', views.process_order, name="process-order"),
    path('order-confirmation/', views.order_confirmation, name="order-confirmation"),
    path('invoice/', views.invoice, name="invoice"),

	path('ajax-add-review/<int:pid>/', views.ajax_add_review, name="ajax-add-review")
]