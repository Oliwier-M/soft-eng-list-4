from django.urls import path
from .views import product_detail, product_list

urlpatterns = [
    path('api/products/<int:product_id>/', product_detail,
    name='product_detail'),
    path('api/products/', product_list,
    name='product_list'),
]