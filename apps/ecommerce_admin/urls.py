from django.urls import path
from apps.ecommerce_admin.models import *
from . import views
urlpatterns = [
    path('', views.admin_login),
    path('process_login', views.process_login),
    path('dashboard/orders', views.orders),
    path('dashboard/orders/show/<int:order_id>', views.show_order),
    path('dashboard/products', views.products),
    path('dashboard/products/edit/<int:id>', views.edit),
    path('dashboard/products/delete/<int:id>', views.delete),
    path('dashboard/products/add', views.add_product),
    path('process_add', views.process_add),
    path('process_edit', views.process_edit),
    path('dashboard/products/add/types/<category>', views.all_types),
    path('dashboard/products/edit/add/types/<category>', views.all_types),
    path('logout', views.logout)
]