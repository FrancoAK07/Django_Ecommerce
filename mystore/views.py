from django.shortcuts import render, redirect
from .models import Product, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import (
    SignUpForm,
    UpdateUserForm,
    ChangePasswordForm,
    UserInfoForm,
    LoginForm,
)
from django.db.models import Q
import json
from shoppingcart.shoppingcart import ShoppingCart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def home(request):
    recent_products = Product.objects.all().order_by("id")[::-1][:3]
    return render(request, "mystore/index.html", {"recent": recent_products})


def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, "mystore/product_details.html", {"product": product})


def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                current_user = Profile.objects.get(user__id=request.user.id)
                saved_cart = current_user.old_cart
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    cart = ShoppingCart(request)
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)

                messages.success(request, ("logged in successfully!"))
                return redirect("home")
            else:
                messages.success(request, ("username or password incorrect"))
                return redirect("login")
        else:
            messages.success(request, ("username or password incorrect"))
            return redirect("login")
    else:
        return render(request, "mystore/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, ("logged out successfully!"))
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("registered successfully!"))
            return redirect("update_info")
        else:
            messages.success(request, ("please check all information is valid!"))
            return redirect("register")
    else:
        return render(request, "mystore/register.html", {"form": form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("Profile updated successfully!"))
            return redirect("home")
        return render(request, "mystore/update_user.html", {"user_form": user_form})
    else:
        messages.success(request, ("Log in to update your profile"))
        return redirect("home")


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Password Updated!"))
                login(request, current_user)
                return redirect("update_user")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password")
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "mystore/update_password.html", {"form": form})

    else:
        messages.success(request, ("Must be logged in"))
        return redirect("Update_password")


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, ("Info updated successfully!"))
            return redirect("home")
        return render(
            request,
            "mystore/update_info.html",
            {"form": form, "shipping_form": shipping_form},
        )
    else:
        messages.success(request, ("Log in to update your info"))
        return redirect("home")


def search_product(request):
    filter_value = request.GET.get("filterValue")
    if request.method == "POST":
        searched = request.POST["searched"]
        if searched != "":
            # query the products model
            searched = Product.objects.filter(
                Q(title__icontains=searched) | Q(description__icontains=searched)
            )
            if not searched:
                messages.success(request, ("No products found"))
                return render(request, "mystore/search.html", {})
            else:
                return render(request, "mystore/search.html", {"searched": searched})
        else:
            messages.success(request, ("No products found"))
            return render(request, "mystore/search.html", {})
    else:
        if filter_value == "all departments":
            filtered = Product.objects.all()
            return render(
                request,
                "mystore/search.html",
                {"filtered": filtered, "department": filter_value.capitalize()},
            )
        elif filter_value != "all":
            filtered = Product.objects.filter(Q(department__icontains=filter_value))
            return render(
                request,
                "mystore/search.html",
                {"filtered": filtered, "department": filter_value.capitalize()},
            )
