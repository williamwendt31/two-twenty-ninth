from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart),
    path('add-product', views.add_product_to_cart),
    path('process-customer-info', views.process_info),
    path('process-payment', views.process_payment),
    path('remove-from-cart/<int:cart_id>', views.remove_from_cart),
    path('checkout', views.checkout)
]