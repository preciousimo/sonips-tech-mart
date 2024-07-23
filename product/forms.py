from django import forms
from django.core.validators import RegexValidator
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Name'}))
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write review'}))

    class Meta:
        model = ProductReview
        fields = ['user_name', 'review', 'rating']

class BillingForm(forms.Form):
    
    PAYMENT_METHOD_CHOICES = [
        ('online_payment', 'Pay Online'),
        ('pay_on_delivery', 'Pay on Delivery'),
    ]

    first_name = forms.CharField(label='Full Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    address = forms.CharField(label='Address', widget=forms.Textarea)
    nearest_bus_stop = forms.CharField(label='Nearest Bus Stop', max_length=100)
    
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
    )
    
    phone_regex = RegexValidator(
        regex=r'^(?:\+234|0)\d{10}$',
        message="Validates number start with +234 or 0, then 10 digits."
    )
    phone_number = forms.CharField(label='Phone Number', validators=[phone_regex])
