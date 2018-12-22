from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('change-order/<sort_by>', views.change_order),
    path('products/show/<int:product_id>', views.show),
    path('products/category/<int:category_id>/', views.category),
    path('products/category/<int:category_id>/change-order/<sort_by>', views.category_sort),
    path('products/category/<int:category_id>/type/<int:type_id>/', views.category_type),
    path('products/category/<int:category_id>/type/<int:type_id>/change-order/<sort_by>', views.category_type_sort),
    path('search/<query>', views.search),
]