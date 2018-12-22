from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from apps.ecommerce_admin.models import *
import json

# serve index page and create uuid 
def index(request):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    products = Product.objects.all()
    categories = Product_Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "shopping_cart": Shopping_Cart.objects.filter(customer_id=request.session['customer_id'])
    }
    return render(request, 'index.html', context)

# show specific product to customer
def show(request, product_id):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    prices = {}
    product = Product.objects.get(id=product_id)
    for i in range(1,6):
        prices[i] = product.price * i
    context = {
        "categories": Product_Category.objects.all(),
        "product": product,
        "prices": prices,
        "shopping_cart": Shopping_Cart.objects.filter(customer_id=request.session['customer_id'])
    }
    return render(request, 'show.html', context)

# all clothes within category
def category(request, category_id):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    products = Product.objects.filter(product_category_id=category_id)
    categories = Product_Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "shopping_cart": Shopping_Cart.objects.filter(customer_id=request.session['customer_id'])
    }
    return render(request, 'index.html', context)

# all clothes within type within categories
def category_type(request, category_id, type_id):
    if 'customer_id' not in request.session:
        request.session['customer_id'] = Shopping_Cart.objects.get_create_customer_id()
    products = Product.objects.filter(product_category_id=category_id).filter(product_type_id=type_id)
    categories = Product_Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "shopping_cart": Shopping_Cart.objects.filter(customer_id=request.session['customer_id'])
    }
    return render(request, 'index.html', context)
    
# sort all clothes
def change_order(request, sort_by):
    return render(request, f'{sort_by}.html', {"products": Product.objects.all()})

# sort all clothes within category
def category_sort(request, category_id, sort_by):
    return render(request, f'{sort_by}.html', {"products": Product.objects.filter(product_category_id=category_id)})

# sort all clothes within type
def category_type_sort(request, category_id, type_id, sort_by):
    return render(request, f'{sort_by}.html', {"products": Product.objects.filter(product_category_id=category_id).filter(product_type_id=type_id)})

# search all clothes
def search(request, query):
    products = Product.objects.filter(name__icontains=query)
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")
