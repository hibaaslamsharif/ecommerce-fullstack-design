from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, product_list, product_detail, 
    cart_view, index_view, checkout_view,
    add_to_cart, update_cart, remove_from_cart, get_cart_count
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Product URLs
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/count/', get_cart_count, name='cart_count'),
    
    # Other URLs
    path('', index_view, name='index'),
    path('checkout/', checkout_view, name='checkout'),
]
