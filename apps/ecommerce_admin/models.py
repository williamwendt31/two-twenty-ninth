from django.db import models
import uuid

import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# skinny controllers fat models 


# manage admin user
class AdminManager(models.Manager):
    def login_validation(self, postData):
        errors = {}
        try:
            user = Admin_User.objects.get(email=postData['email'])
        except Admin_User.DoesNotExist:
            user = None
        if not user or not bcrypt.checkpw(postData['pwd'].encode('utf-8'), user.pwd_hash.encode('utf-8')):
            errors['invalid'] = "Invalid Credentials"
        return errors

    def register_user(self):
        hashed_password = bcrypt.hashpw('user'.encode('utf-8'), bcrypt.gensalt()).decode()
        Admin_User.objects.create(first_name="William", last_name="Wendt", email="user", pwd_hash=hashed_password)
        return

# manage products
class ProductManager(models.Manager):
    def get_category_and_type(self, postData):
        if 'prod_category' in postData and len(postData['prod_category']):
            category = postData['prod_category']
        else:
            category = postData['new_category']
        if 'prod_type' in postData and len(postData['prod_type']):
            prod_type = postData['prod_type']
        else:
            prod_type = postData['new_type']
        prod_cat_type = {
            "category": category,
            "type": prod_type
        }
        return prod_cat_type

    def input_validation(self, postData):
        errors = {}
        prod_cat_type = Product.objects.get_category_and_type(postData)
        category = prod_cat_type['category']
        prod_type = prod_cat_type['type']
        if not len(postData['prod_name']) or not len(postData['price']) or not len(postData['desc']) or not len(category) or not len(prod_type) or not len(postData['image']): #if any are empty
            errors['required'] = "All fields required"
            return errors
        price = float(postData['price'])
        if price < 0.99:
            errors['little'] = "Price Field must be at least 1 dollar"
        return errors

    def add_product(self, postData):
        prod_cat_type = Product.objects.get_category_and_type(postData)
        try:
            # old category
            category = Product_Category.objects.get(name=prod_cat_type['category'])
        except Product_Category.DoesNotExist:
            # new category
            category = Product_Category.objects.create(name=prod_cat_type['category'])
        try:
            # old type
            prod_type = Product_Category.objects.get(name=prod_cat_type['category']).types.all().get(name=prod_cat_type['type'])
        except Product_Type.DoesNotExist:
            #new type
            prod_type = Product_Type.objects.create(name=prod_cat_type['type'], category=category)
        new_product = Product.objects.create(name=postData['prod_name'], price=postData['price'], desc=postData['desc'], image=postData['image'], product_type=prod_type, product_category=category)
        return

    def delete_product(self, id):
        Product.objects.get(id=id).delete()
        return
    
    def update_products(self, cart):
        for item in cart:
            item.product.quantity_sold += item.quantity
            item.product.inventory_count -= item.quantity
            item.product.save()
        return

    def edit_product(self, postData):
        prod = Product.objects.get(id=postData['product_id'])
        prod.name = postData['prod_name']
        prod.price = postData['price']
        prod.desc = postData['desc']
        prod.product_category = Product_Category.objects.get(name=postData['prod_category'])
        prod.product_type = Product_Category.objects.get(name=postData['prod_category']).types.all().get(name=postData['prod_type'])
        prod.save()
        return

# manage orders
class OrderManager(models.Manager):
    def add_order(self, customer_id, cart):
        order = Order.objects.create(customer_id=customer_id, shipping_info=ShippingCustomer.objects.filter(customer_id=customer_id).last(), billing_info=BillingCustomer.objects.filter(customer_id=customer_id).last(),total=0, status="Order in Process")
        total = 0
        for item in cart:
            order.shopping_cart.add(item)
            total += item.total
        order.total = total
        order.save()
        return

# manage shoppping cart
class Shopping_CartManager(models.Manager):
    def customer_info_validation(self, postData):
        errors = {}
        for key in postData:
            if not len(postData[key]):
                errors['required'] = 'All fields required'
        return errors

    def get_create_customer_id(self):   
        return uuid.uuid4().hex

    def add_to_cart(self, customer_id, product_id, quantity):
        product = Product.objects.get(id=product_id)
        total = float(product.price) * float(quantity)
        Shopping_Cart.objects.create(customer_id=customer_id, product=product, quantity=float(quantity), total=total)
        return

    def update_cart(self, cart_id, quantity):
        entry = Shopping_Cart.objects.get(id=cart_id)
        entry.quantity = quantity
        entry.total = entry.product['price'] * quantity
        entry.save()
        return
    
    def remove_from_cart(self, cart_id):
        Shopping_Cart.objects.get(id=cart_id).delete()
        return

    def delete_all_instances(self, customer_id):
        all_entries = Shopping_Cart.objects.filter(customer_id=customer_id)
        all_entries.delete()
        return

    def add_customer_info(self, customer_id, postData):
        ship_addr = Address.objects.create(customer_id=customer_id, address=postData['s_address'], city=postData['s_city'], state=State.objects.get(name=postData['s_state']), zipcode=postData['s_zipcode'])
        ShippingCustomer.objects.create(customer_id=customer_id, first_name=postData['s_first_name'], last_name=postData['s_last_name'], address=ship_addr)
        if 'same' in postData:
            BillingCustomer.objects.create(customer_id=customer_id, first_name=postData['s_first_name'], last_name=postData['s_last_name'], address=ship_addr)
        else:
            bill_addr = Address.objects.create(customer_id=customer_id, address=postData['b_address'], city=postData['b_city'], state=State.objects.get(name=postData['b_state']), zipcode=postData['b_zipcode'])
            BillingCustomer.objects.create(customer_id=customer_id, first_name=postData['s_first_name'], last_name=postData['b_last_name'], address=bill_addr)
        return


class Admin_User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100, unique=True)
    pwd_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()

class Product_Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product_Type(models.Model):
    name = models.CharField(max_length=60)
    category = models.ForeignKey(Product_Category, on_delete=models.CASCADE, related_name="types")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    desc = models.TextField(max_length=300)
    image = models.TextField()
    inventory_count = models.IntegerField(default=200)
    quantity_sold = models.IntegerField(default=0)
    product_type = models.ForeignKey(Product_Type, on_delete=models.CASCADE, related_name="product")
    product_category = models.ForeignKey(Product_Category, on_delete=models.CASCADE, related_name="product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

class State(models.Model):
    name = models.CharField(max_length=60)

class Address(models.Model):
    customer_id = models.CharField(max_length=255)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BillingCustomer(models.Model):
    customer_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShippingCustomer(models.Model):
    customer_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shopping_Cart(models.Model):
    customer_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Shopping_CartManager()

class Order(models.Model):
    customer_id = models.CharField(max_length=255)
    shipping_info = models.ForeignKey(ShippingCustomer, on_delete=models.CASCADE, related_name="order")
    billing_info = models.ForeignKey(BillingCustomer, on_delete=models.CASCADE, related_name="order")
    shopping_cart = models.ManyToManyField(Shopping_Cart, related_name="order")
    total = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrderManager()