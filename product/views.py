from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Avg, FloatField
from django.db.models.functions import Cast
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from product.models import Product, Category, ProductImages, CartOrder, CartOrderItems, ProductReview, Coupon, Wishlist
from userauths.models import User
from .forms import ProductReviewForm, BillingForm
from .pdf import html2pdf
from io import BytesIO

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

    products = Product.objects.filter(
        category=product.category).exclude(pid=pid)

    total_products = len(products)
    num_products = min(total_products, 4)
    productss = random.sample(list(products), num_products)

    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg(Cast('rating', output_field=FloatField())))

    review_form = ProductReviewForm()
    p_image = product.p_images.all()

    context = {
        "p": product,
        "review_form": review_form,
        "reviews": reviews,
        "average_rating": average_rating,
        "p_image": p_image,
        "products": productss,
    }

    return render(request, "product/product_detail.html", context)


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("date")
    context = {
        "products": products,
        "query": query,
    }

    return render(request, "product/product_list.html", context)


def cart(request):
    cart_total_amount = 0
    coupon_discount = 0
    delivery_fee = 1500

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        if request.method == 'POST':
            coupon_code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                coupon_discount = coupon.amount
                messages.success(request, "Coupon applied successfully!")
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code!")

        total_amount = cart_total_amount - coupon_discount + delivery_fee

        return render(request, "product/cart.html", {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'coupon_discount': coupon_discount,
            'delivery_fee': delivery_fee,
            'total_amount': total_amount
        })
    else:
        messages.warning(request, "Your cart is empty!")
        return redirect('/')



def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("product/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(
        request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("product/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(
        request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

@login_required(login_url='login')
def checkout(request):
    cart_total_amount = 0
    delivery_fee = 1500  # Add the delivery fee here

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        country_choices = CartOrder._meta.get_field('country').choices
        state_choices = CartOrder._meta.get_field('state').choices

        # Get the active coupon, if any
        active_coupon = Coupon.objects.filter(active=True).first()

        # Calculate the total amount
        if active_coupon:
            total_amount = cart_total_amount - active_coupon.amount + delivery_fee
        else:
            total_amount = cart_total_amount + delivery_fee

        return render(request, "product/checkout.html", {
            "cart_data": request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']), 
            'cart_total_amount': cart_total_amount,
            'country_choices': country_choices,
            'state_choices': state_choices,
            'active_coupon': active_coupon,
            'delivery_fee': delivery_fee,
            'total_amount': total_amount
        })
    else:
        messages.warning(request, "Your cart is empty!")
        return redirect('/')

    

def process_order(request):
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        cart_total_amount = 0
        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        if request.method == 'POST':
            # Process the form submission with billing details
            form = BillingForm(request.POST)
            if form.is_valid():
                # Save the billing details and create an order
                billing_data = form.cleaned_data
                user = request.user
                order = CartOrder.objects.create(
                    user_id=user.id, 
                    first_name=billing_data['first_name'],
                    last_name=billing_data['last_name'],
                    email=billing_data['email'],
                    country=billing_data['country'],
                    state=billing_data['state'],
                    nearest_bus_stop=billing_data['nearest_bus_stop'],
                    address=billing_data['address'],
                    phone_number=billing_data['phone_number'],
                    price=cart_total_amount,
                    payment_method='Pay on Delivery',
                )

                # Save the order items
                for p_id, item in cart_data.items():
                    product = Product.objects.get(pid=item['pid'])
                    CartOrderItems.objects.create(
                        order=order,
                        product=product,
                        invoice_no='INVOICE_NO-' + str(order.id),
                        item=item['title'],
                        image=item['image'],
                        qty=item['qty'],
                        price=item['price'],
                        total=float(item['qty']) + float(item['price'])
                    )

                # Clear the cart data from the session
                # del request.session['cart_data_obj']

                # Create the invoice using a template
                context = {
                    'order': order,
                    'cart_data': cart_data,
                    'totalcartitems': len(request.session['cart_data_obj']),
                    'cart_total_amount': cart_total_amount,
                }

                invoice_html = html2pdf('product/invoice.html', context)

                subject = 'Invoice for your order'
                message = 'Please find attached the invoice for your order. This is a no reply mail but you can contact us through support@sonipstechmart.com for any enquiry.'
                from_email = settings.EMAIL_HOST_USER
                to_email = order.email

                # Convert invoice_html to a File object
                invoice_file = BytesIO(invoice_html)

                email = EmailMessage(subject, message, from_email, [to_email])
                email.attach(
                    'invoice.pdf', invoice_file.getvalue(), 'application/pdf')
                email.send()

                subject_ = 'Notice for an order'
                message_ = f'Please find notice information for { order.full_name } new order.'
                from_email_ = order.email
                to_email_ = settings.EMAIL_HOST_USER

                notice = EmailMessage(subject_, message_,
                                      from_email_, [to_email_])
                notice.attach(
                    'invoice.pdf', invoice_file.getvalue(), 'application/pdf')
                notice.send()

                # Clear the cart data from the session
                del request.session['cart_data_obj']

                return redirect('order-confirmation')

        else:
            form = BillingForm()

        return render(request, 'product/checkout.html', {
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount,
            'form': form,
        })
    else:
        messages.warning(request, "Your cart is empty!")
        return redirect('/products/')


def order_confirmation(request):

    context = {
        'redirect_delay': 5,  # Delay in seconds
    }

    return render(request, 'product/order-confirmation.html', context)


def invoice(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

        order = CartOrder.objects.all()

    return render(request, "product/invoice.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'order': order})


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)

    reviews = ProductReview.objects.create(
        product=product,
        name=request.POST['name'],
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context = {
        'name': request.POST['name'],
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
)
