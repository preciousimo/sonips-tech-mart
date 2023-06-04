from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  


# Create your forms here.

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class":"form-control rounded-input", 'placeholder':'Username'}))
	email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class":"form-control rounded-input", 'placeholder':'Email'})) 
	password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={"class":"form-control rounded-input", 'placeholder':'Password'}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class":"form-control rounded-input", 'placeholder':'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ["username", "email"]
		
	
	def username_clean(self):  
		username = self.cleaned_data['username'].lower()  
		new = User.objects.filter(username = username)  
		if new.count():  
			raise ValidationError("User Already Exist")  
		return username  
	
	def email_clean(self):  
		email = self.cleaned_data['email'].lower()  
		new = User.objects.filter(email=email)  
		if new.count():  
			raise ValidationError(" Email Already Exist")  
		return email  
	
	def clean_password2(self):  
		password1 = self.cleaned_data['password1']  
		password2 = self.cleaned_data['password2']  
		if password1 and password2 and password1 != password2:  
			raise ValidationError("Password don't match")  
		return password2
	
	def save(self, commit=True):  
		user = User.objects.create_user(  
			self.cleaned_data['username'],  
			self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )
		if commit:
			user.save()
		return user