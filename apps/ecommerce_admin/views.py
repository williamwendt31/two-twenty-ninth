from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core import serializers
from .models import *
import re, bcrypt

# serve login page
def admin_login(request):
    return render(request, 'admin.html')

# process login and either redirect after success or serve errors
def process_login(request):
    if request.method == 'POST':
        errors = Admin_User.objects.login_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/admin')
        user = Admin_User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id     
    return redirect('/admin/dashboard/orders')

# show all orders
def orders(request):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    context = {
        "orders": Order.objects.all()
    }
    return render(request, 'admin_dashboard.html', context)

# show all products && dynamic pagination
def products(request):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    product_list = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'admin_products.html', {"products": products})

# show specific order details
def show_order(request, order_id):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    context = {
        "order": Order.objects.get(id=order_id)
    }
    print(Order.objects.get(id=order_id).shopping_cart.values())
    return render(request, 'show_order.html', context)

# edit product form
def edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    context = {
        "product": Product.objects.get(id=id),
        "categories": Product_Category.objects.all()
    }
    return render(request, 'edit_product.html', context)

# remove product 
def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    Product.objects.delete_product(id)
    return redirect('/admin/dashboard/products')

# serve add product form
def add_product(request):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    context = {
        "categories": Product_Category.objects.all()
    }
    return render(request, 'add_product.html', context)

# process adding product
def process_add(request):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    if request.method == 'POST':
        errors = Product.objects.input_validation(request.POST, request.FILES)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/admin/dashboard/products/add')
        Product.objects.add_product(request.POST, request.FILES)
    return redirect('/admin/dashboard/products')

# process editing product
def process_edit(request):
    if 'user_id' not in request.session:
        return redirect('/admin/logout')
    if request.method == 'POST':
        Product.objects.edit_product(request.POST)
    return redirect('/admin/dashboard/products')

# all types in category
def all_types(request, category):
    types = Product_Type.objects.filter(category=Product_Category.objects.get(name=category))
    if len(types) == 0:
        return HttpResponse("")
    return HttpResponse(serializers.serialize("json", types), content_type="application/json")

# log user out
def logout(request):
    request.session.clear()
    return redirect('/admin')
