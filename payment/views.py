from django.shortcuts import render, redirect
from shoppingcart.shoppingcart import ShoppingCart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from mystore.models import Product, Profile
import datetime


def payment_success(request):
    return render(request, "payment/payment_success.html", {})


def checkout(request):
    cart = ShoppingCart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    totals = cart.cart_total()
    total_prices = {}
    for product, qty in cart.cart.items():
        if product not in total_prices:
            for item in cart_products():
                if int(product) == int(item.id):
                    total_prices[product] = round(float(qty) * float(item.price), 2)

    if request.user.is_authenticated:
        # Checkout as logged in user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        billing_form = PaymentForm()
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
                "prices": total_prices,
                "billing_form": billing_form,
            },
        )
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        billing_form = PaymentForm()
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_form": shipping_form,
                "prices": total_prices,
                "billing_form": billing_form,
            },
        )


def billing_info(request):
    if request.POST:
        cart = ShoppingCart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        totals = cart.cart_total()
        shipping_form = request.POST
        my_shipping = request.POST
        request.session["my_shipping"] = my_shipping
        total_prices = {}
        for product, qty in cart.cart.items():
            if product not in total_prices:
                for item in cart_products():
                    if int(product) == int(item.id):
                        total_prices[product] = round(float(qty) * float(item.price), 2)

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(
                request,
                "payment/billing_info.html",
                {
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "shipping_info": shipping_form,
                    "billing_form": billing_form,
                    "prices": total_prices,
                },
            )
        else:
            billing_form = PaymentForm()
            return render(
                request,
                "payment/billing_info.html",
                {
                    "cart_products": cart_products,
                    "quantities": quantities,
                    "totals": totals,
                    "shipping_info": shipping_form,
                    "billing_form": billing_form,
                    "prices": total_prices,
                },
            )
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def process_order(request):
    my_shipping = request.session.get("my_shipping")
    if request.session.get("my_shipping"):

        billing_info = {}
        for key, value in my_shipping.items():
            if "card" in key:
                billing_info[key] = value
        for key, value in billing_info.items():
            if key != "card_address2":
                if value != "":
                    cart = ShoppingCart(request)
                    cart_products = cart.get_products
                    quantities = cart.get_quants
                    totals = cart.cart_total()
                    payment_form = PaymentForm(request.POST or None)
                    full_name = my_shipping["shipping_full_name"]
                    email = my_shipping["shipping_email"]
                    amount_paid = totals
                    shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
                    if request.user.is_authenticated:
                        user = request.user
                        create_order = Order(
                            user=user,
                            full_name=full_name,
                            email=email,
                            shipping_address=shipping_address,
                            amount_paid=amount_paid,
                        )
                        create_order.save()
                        order_id = create_order.pk

                        for product in cart_products():
                            product_id = product.id
                            price = product.price

                            for key, value in quantities().items():
                                if int(key) == product.id:
                                    create_order_item = OrderItem(
                                        order_id=order_id,
                                        product_id=product_id,
                                        user=user,
                                        quantity=value,
                                        price=price,
                                    )
                                    create_order_item.save()

                        for key in list(request.session.keys()):
                            if key == "session_key":
                                del request.session[key]

                        current_user = Profile.objects.filter(user__id=request.user.id)
                        current_user.update(old_cart="")

                        del request.session["my_shipping"]
                        messages.success(request, "Order Placed")
                        return redirect("home")
                    else:
                        create_order = Order(
                            full_name=full_name,
                            email=email,
                            shipping_address=shipping_address,
                            amount_paid=amount_paid,
                        )
                        create_order.save()
                        order_id = create_order.pk

                        for product in cart_products():
                            product_id = product.id
                            price = product.price

                            for key, value in quantities().items():
                                if int(key) == product.id:
                                    create_order_item = OrderItem(
                                        order_id=order_id,
                                        product_id=product_id,
                                        quantity=value,
                                        price=price,
                                    )
                                    create_order_item.save()

                        for key in list(request.session.keys()):
                            if key == "session_key":
                                del request.session[key]

                        del request.session["my_shipping"]
                        messages.success(request, "Order Placed")
                        return redirect("home")
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST["shipping_status"]
            num = request.POST["num"]
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request, "shipping status updated")
            return redirect("home")
        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST["shipping_status"]
            num = request.POST["num"]
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "shipping status updated")
            return redirect("home")
        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST["shipping_status"]
            if status == "true":
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "shipping status updated")
            return redirect("home")
        else:
            pass
        return render(request, "payment/orders.html", {"order": order, "items": items})
    else:
        messages.success(request, "Access Denied")
        return redirect("home")
