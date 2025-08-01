from django.shortcuts import render, get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# HTML view: product list
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/productlist.html', {'products': products})

# HTML view: product detail
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

# API view: product list
@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# API view: product detail
@api_view(['GET'])
def api_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
def cart_view(request):
    return render(request, 'store/cart.html')
def index_view(request):
    return render(request, 'store/index.html')

def checkout_view(request):
    return render(request, 'store/checkout.html')
