from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=True)
            username = form.cleaned_data['username']
            messages.success(request, f"New Account Created: {username}")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('/')
    else:
        form =  UserRegisterForm()
    context = {'form': form}
    return render(request, "userauths/signup.html", context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {email}. You are now logged in.")
                return redirect('/')
            else:
                messages.warning(request, "User does not exist, create an account.")
                
        except:
            messages.warning(request, f'User with {email} does not exist')

    return render(request, 'userauths/login.html')