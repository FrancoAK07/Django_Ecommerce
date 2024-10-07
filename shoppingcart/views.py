from django.shortcuts import render, get_object_or_404
from .shoppingcart import ShoppingCart
from mystore.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = ShoppingCart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    total_prices = {}
    for product, qty in cart.cart.items():
        if product not in total_prices:
            for item in cart_products():
                if int(product) == int(item.id):
                    total_prices[product] = round(float(qty) * float(item.price), 2)
    totals = cart.cart_total()
    return render(request, "shoppingcart/cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "prices":total_prices})


def cart_add(request):
    cart = ShoppingCart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty})
        messages.success(request, ("Product added to cart"))
        return response

def cart_delete(request):
    cart = ShoppingCart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)
        response = JsonResponse({"product": product_id})
        messages.success(request, ("Product removed from cart"))
        return response

def cart_update(request):
    cart = ShoppingCart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({"qty": product_qty})
        return response


