from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICES = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

RATING = (
    ('1', '⭐✰✰✰✰'),
    ('2', '⭐⭐✰✰✰'),
    ('3', '⭐⭐⭐✰✰'),
    ('4', '⭐⭐⭐⭐✰'),
    ('5', '⭐⭐⭐⭐⭐'),
)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdjefgh12345")
    title = models.CharField(max_length=100, default="category group")
    image = models.ImageField(upload_to="category", default="category.jpg")
    parent_category = models.ForeignKey("self", blank=True, null=True, related_name="children_categories", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdjefgh12345")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='item')
    title = models.CharField(max_length=100, default="Product name")
    image = models.ImageField(upload_to="products", default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default="2.99")
    specifications = models.TextField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Products'


    def __str__(self):
        return self.title
    
    def product_image(self):
        if self.image:
            return mark_safe('<img src="%s" width="100" height="100" />' % (self.image.url))
        else:
            return 'No Image Found'
    
    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return int(new_price)
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="p_image", on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product_images', default="avatar.png", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'
    

class CartOrder(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('pay_on_delivery', 'Pay on Delivery'),
        ('online_payment', 'Online Payment'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='pay_on_delivery')
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing')

    class Meta:
        verbose_name_plural = 'Cart Order'

    def __str__(self):
        return f"Order #{self.pk}"
    
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=200, null=True)
    qty = models.PositiveIntegerField(default=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def order_img(self):
        if self.image:
            return mark_safe('<img src="%s" width="100" height="100" />' % (self.image.url))
        else:
            return 'No Image Found'
           
    def __str__(self):
        return f"{self.qty} x {self.product.title} - {self.price}"

 
class ProductReview(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="review")
    review = models.TextField()
    rating = models.CharField(choices=RATING, default=None, max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title
    
    def get_ratting(self):
        return self.rating
    

class Wishlist(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="wishlist")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'