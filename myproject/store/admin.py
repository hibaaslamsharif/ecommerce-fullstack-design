from django.contrib import admin
from .models import Product, Cart, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category')
    list_editable = ('price', 'is_active')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Images', {
            'fields': ('image', 'image_2', 'image_3', 'image_4'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 20
    ordering = ('-created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'get_total_items')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_total_items(self, obj):
        return obj.items.count()
    get_total_items.short_description = 'Total Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_total_price')
    list_filter = ('cart__created_at',)
    search_fields = ('product__name', 'cart__user__username')
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'
