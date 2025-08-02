from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
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
def get_cart_data(cart):
    cart_items = []
    total_price = 0
    
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = float(item['price']) * item['quantity']
            total_price += item_total
            
            cart_items.append({
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': float(item['price']),
                    'image': product.image
                },
                'quantity': item['quantity'],
                'total': item_total
            })
        except (Product.DoesNotExist, ValueError) as e:
            print(f"Error processing cart item {product_id}: {e}")
            continue
    
    # Debug output
    print(f"Processed {len(cart_items)} cart items")
    print(f"Cart items: {cart_items}")
    
    shipping = 0 if total_price == 0 else 10  # Example shipping cost
    tax = round(total_price * 0.05, 2)
    total = total_price + shipping + tax
    return {
        'cart_items': cart_items,
        'total_price': total_price,
        'subtotal': total_price,
        'shipping': shipping,
        'tax': tax,
        'total': total
    }

def cart_view(request):
    # Debug session data
    print("Session data:", dict(request.session))
    print("Session key:", request.session.session_key)
    
    cart = request.session.get('cart', {})
    print("Raw cart data from session:", cart)
    
    context = get_cart_data(cart)
    print("Processed cart context:", context)
    
    return render(request, 'store/cart.html', context)

@require_POST
def add_to_cart(request, product_id):
    try:
        # Get or initialize cart in session
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        product = get_object_or_404(Product, id=product_id)
        
        # Debug output
        print(f"Adding product {product_id} to cart. Current cart before update: {cart}")
        
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'quantity': 1,
                'name': product.name,
                'price': str(product.price)
            }
        
        # Save the cart back to session
        request.session['cart'] = cart
        request.session.modified = True  # Make sure to save the session
        
        # Debug output
        print(f"Cart after adding product {product_id}: {cart}")
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"{product.name} added to cart!",
                'cart_count': sum(item['quantity'] for item in cart.values())
            })
        
        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')
        
    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        messages.error(request, "An error occurred while adding the item to cart.")
        return redirect('product_detail', id=product_id)

@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = request.POST.get('quantity')
    
    try:
        quantity = int(quantity)
        if quantity > 0:
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] = quantity
                request.session['cart'] = cart
                messages.success(request, 'Cart updated successfully!')
        else:
            remove_from_cart(request, product_id)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity')
    
    return redirect('cart')

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        product_name = cart[str(product_id)]['name']
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, f"{product_name} removed from cart!")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({'success': True, 'message': f"{product_name} removed from cart!"})
    return redirect('cart')

def get_cart_count(request):
    """API endpoint to get the current cart item count"""
    cart = request.session.get('cart', {})
    total_items = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': total_items})
def index_view(request):
    return render(request, 'store/index.html')

def checkout_view(request):
    cart = request.session.get('cart', {})
    context = get_cart_data(cart)
    return render(request, 'store/checkout.html', context)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer