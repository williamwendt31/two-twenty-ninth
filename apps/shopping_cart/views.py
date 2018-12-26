from django.shortcuts import render, HttpResponse, redirect
from apps.ecommerce_admin.models import *
from django.contrib import messages

import stripe

stripe.api_key = "sk_test_7uJwPysNuUKFf1rD3B23imAi"

# items in cart && keeps track using session (holding uuid)
def cart(request):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()

    categories = Product_Category.objects.all()
    cart =  Shopping_Cart.objects.filter(customer_id=request.session['customer_id'])
    cart_total = 0
    for item in cart:
        cart_total += item.total
    try:
        customer_shipping = ShippingCustomer.objects.filter(customer_id=request.session['customer_id']).last()
    except ShippingCustomer.DoesNotExist:
        customer_shipping = None
    try:
        customer_billing = BillingCustomer.objects.filter(customer_id=request.session['customer_id']).last()
    except BillingCustomer.DoesNotExist:
        customer_billing = None

    context = {
        "categories": categories,
        "shopping_cart": cart,
        "cart_total": cart_total,
        "states": State.objects.all(),
        "customer_shipping": customer_shipping,
        "customer_billing": customer_billing
    }
    return render(request, 'cart.html', context)

# add item to cart
def add_product_to_cart(request):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()

    if request.method == 'POST':
        Shopping_Cart.objects.add_to_cart(request.session['customer_id'], request.POST['product_id'], request.POST['product_quantity'])
    return redirect(f"/products/show/{request.POST['product_id']}")

# remove item from cart
def remove_from_cart(request, cart_id):
    Shopping_Cart.objects.remove_from_cart(cart_id=cart_id)
    return redirect('/shopping-cart')
    
# process customer shipping && billing info
def process_info(request):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    
    if request.method == 'POST':
        errors = Shopping_Cart.objects.customer_info_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/shopping-cart')
        Shopping_Cart.objects.add_customer_info(request.session['customer_id'], request.POST)
        return redirect('/shopping-cart/checkout')
    return redirect('/shopping-cart')

# server checkout with all items in cart
def checkout(request):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()

    categories = Product_Category.objects.all()
    cart =  Shopping_Cart.objects.filter(customer_id=request.session['customer_id'])
    cart_total = 0

    for item in cart:
        cart_total += item.total
    customer_shipping = ShippingCustomer.objects.filter(customer_id=request.session['customer_id']).last()
    customer_billing = BillingCustomer.objects.filter(customer_id=request.session['customer_id']).last()

    context = {
        "categories": categories,
        "shopping_cart": cart,
        "cart_total": cart_total,
        "states": State.objects.all(),
        "customer_shipping": customer_shipping,
        "customer_billing": customer_billing
    }
    return render(request, 'checkout.html', context)

# process all items in cart and customer info
def process_payment(request):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    print(request.session['customer_id'])
    messages.success(request, "Congratulations your order has been placed! Order confirmation has been sent to your email")
    Product.objects.update_products(Shopping_Cart.objects.filter(customer_id=request.session['customer_id']))
    Order.objects.add_order(request.session['customer_id'], Shopping_Cart.objects.filter(customer_id=request.session['customer_id']))
    request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    print(request.session['customer_id'])
    return redirect('/')
