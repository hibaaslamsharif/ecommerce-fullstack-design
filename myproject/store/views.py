from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
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
                request.session.modified = True
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Cart updated successfully!',
                        'cart_count': sum(item['quantity'] for item in cart.values())
                    })
                else:
                    messages.success(request, 'Cart updated successfully!')
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'Product not found in cart'
                    })
                else:
                    messages.error(request, 'Product not found in cart')
        else:
            return remove_from_cart(request, product_id)
    except (ValueError, TypeError):
        error_msg = 'Invalid quantity'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_msg
            })
        else:
            messages.error(request, error_msg)
    
    return redirect('cart')

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        product_name = cart[str(product_id)]['name']
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'message': f"{product_name} removed from cart!",
                'cart_count': sum(item['quantity'] for item in cart.values())
            })
        else:
            messages.success(request, f"{product_name} removed from cart!")
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False, 
                'error': 'Product not found in cart'
            })
        else:
            messages.error(request, 'Product not found in cart')
    
    return redirect('cart')

def get_cart_count(request):
    """API endpoint to get the current cart item count"""
    cart = request.session.get('cart', {})
    total_items = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': total_items})
def index_view(request):
    # Get all active products
    products = Product.objects.filter(is_active=True)
    
    # Group products by category
    categories = {}
    for product in products:
        category = product.category
        if category not in categories:
            categories[category] = []
        categories[category].append(product)
    
    # Get featured products (latest 4 products)
    featured_products = products.order_by('-created_at')[:4]
    
    # Get products for different sections
    electronics_products = products.filter(category__icontains='electronics')[:4]
    home_products = products.filter(category__icontains='home')[:4]
    
    # Get deals and offers products specifically
    deals_products = products.filter(category__icontains='deals')[:5]
    if not deals_products.exists():
        deals_products = products.filter(category__icontains='offers')[:5]
    if not deals_products.exists():
        # If no deals category, use featured products for deals section
        deals_products = featured_products[:5]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'electronics_products': electronics_products,
        'home_products': home_products,
        'deals_products': deals_products,
        'all_products': products,
    }
    
    return render(request, 'store/index.html', context)

def checkout_view(request):
    cart = request.session.get('cart', {})
    context = get_cart_data(cart)
    return render(request, 'store/checkout.html', context)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@csrf_exempt
@require_POST
def search_products(request):
    """Search products by name or category"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        category = data.get('category', '').strip()
        
        # Start with all products
        products = Product.objects.filter(is_active=True)
        
        # Filter by category if specified
        if category:
            products = products.filter(category__icontains=category)
        
        # Filter by search query if specified
        if query:
            products = products.filter(name__icontains=query)
        
        # Limit results to 20 products
        products = products[:20]
        
        # Prepare results
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'image': product.image,
                'category': product.category
            })
        
        return JsonResponse({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)