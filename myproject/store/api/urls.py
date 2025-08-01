from django.urls import path
from store.views import api_product_list, api_product_detail

urlpatterns = [
    path('products/', api_product_list, name='api_product_list'),
    path('products/<int:pk>/', api_product_detail, name='api_product_detail'),
]
