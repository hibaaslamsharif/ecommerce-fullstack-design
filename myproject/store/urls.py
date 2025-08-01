from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, product_list, product_detail,cart_view,index_view, checkout_view
router = DefaultRouter()
router.register(r'products', ProductViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('products/', product_list, name='product_list'),
    path('products/<int:id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('', index_view, name='index'),           # http://127.0.0.1:8000/cart/
    path('checkout/', checkout_view, name='checkout'),
       

]
