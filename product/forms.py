from django import forms
from .models import ProductReview



class ProductReviewForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter Name"}))
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = ProductReview
        fields = ['name', 'review', 'rating']