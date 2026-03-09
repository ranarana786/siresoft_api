"""
Cart Admin Configuration
"""
from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline display for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ['unit_price', 'get_total_price']
    fields = ['product', 'service', 'unit_price', 'get_total_price']
    
    def get_total_price(self, obj):
        if obj.pk:
            return f'${obj.get_total_price()}'
        return '-'
    get_total_price.short_description = 'Total'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart"""
    list_display = ['id', 'get_owner', 'get_items_count', 'get_total', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_owner(self, obj):
        if obj.user:
            return f'{obj.user.get_full_name()}'
        return "Anonymous"
    get_owner.short_description = 'Owner'
    
    def get_items_count(self, obj):
        return obj.get_total_items()
    get_items_count.short_description = 'Items'
    
    def get_total(self, obj):
        return f'${obj.get_total_price()}'
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for CartItem"""
    list_display = ['id', 'cart', 'get_item_name', 'get_item_type', 'unit_price', 'get_total']
    list_filter = ['created_at']
    search_fields = ['product__name', 'service__name']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price']
    
    def get_item_name(self, obj):
        return obj.get_item_name()
    get_item_name.short_description = 'Item'
    
    def get_item_type(self, obj):
        return 'Product' if obj.is_product() else 'Service'
    get_item_type.short_description = 'Type'
    
    def get_total(self, obj):
        return f'${obj.get_total_price()}'
    get_total.short_description = 'Total'