from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.product_list, name="product_list"),
    path('product/<pid>/', views.product_detail, name="product-detail"),

	path('search/', views.search_view, name="search"),

]