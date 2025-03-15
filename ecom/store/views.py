from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Product
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm



# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))

            # Check if the user is a seller
            if user.groups.filter(name='Seller').exists():
                return redirect('product_management')
            
            return redirect('home')
        
        else:
            messages.success(request, ("There was an error, please try again...!"))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have Registered Successufully"))
            return redirect('home')
        else:
            messages.success(request, ("Oops! There was a problem! Please Try again"))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})

def is_seller(user):
    return user.groups.filter(name='Seller').exists()

@login_required
@user_passes_test(is_seller)
def product_management(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'product_management.html', {'products': products})

@login_required
@user_passes_test(is_seller)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user) 
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
@user_passes_test(is_seller)
def add_product(request):
    if not request.user.groups.filter(name='Seller').exists():
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user 
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_management')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})

@login_required
@user_passes_test(is_seller)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('product_management')