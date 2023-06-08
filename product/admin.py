from django.contrib import admin
from .models import Category, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ["title", "product_image", "price"]

class CategoryAdmin(admin.ModelAdmin): 
    list_display = ["title"]

class CartOrderAdmin(admin.ModelAdmin): 
    list_editable = ["paid_status", "product_status"]
    list_display = ["full_name", "price", "paid_status", "order_date", "product_status"]

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "invoice_no", "item", "image", "qty", "price", "total"]

class ProductReviewAdmin(admin.ModelAdmin): 
    list_display = ["user", "product", "review", "rating"]

class WishlistAdmin(admin.ModelAdmin): 
    list_display = ["user", "product", "date"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin) 
admin.site.register(Wishlist, WishlistAdmin) 
