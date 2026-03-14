"""
Order and Payment Admin Configuration
Professional admin interface for order management (services/digital products)
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order, OrderItem, Payment, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    """Inline display for order items (quantity removed)"""
    model = OrderItem
    extra = 0
    readonly_fields = ['item_name', 'item_type', 'unit_price', 'total_price']
    fields = ['item_name', 'item_type', 'unit_price', 'total_price', 'custom_requirements']
    can_delete = False


class PaymentInline(admin.TabularInline):
    """Inline display for payments"""
    model = Payment
    extra = 0
    readonly_fields = ['payment_id', 'amount', 'status', 'payment_method', 'created_at']
    fields = ['payment_id', 'amount', 'currency', 'payment_method', 'status', 'created_at']
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    """Inline display for status history"""
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['old_status', 'new_status', 'changed_by', 'created_at']
    fields = ['old_status', 'new_status', 'changed_by', 'notes', 'created_at']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order – shipping, billing, tax fields removed"""
    list_display = [
       'id', 'order_number', 'user', 'status_badge', 'payment_status_badge',
        'total_display', 'created_at'
    ]
    list_filter = [
        'status', 'payment_status', 'payment_method', 'created_at'
    ]
    search_fields = [
        'order_number', 'user__email'
    ]
    date_hierarchy = 'created_at'
    readonly_fields = [
        'order_number', 'created_at', 'updated_at',
        'paid_at', 'delivered_at'
    ]  # user ko hata diya
    inlines = [OrderItemInline, PaymentInline, OrderStatusHistoryInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'total')
        }),
        ('Payment', {
            'fields': ('payment_method',)
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 'updated_at', 'paid_at', 'delivered_at'
            ),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """Display status with color coding (shipped removed)"""
        colors = {
            'pending': '#FFA500',
            'confirmed': '#4169E1',
            'processing': '#1E90FF',
            'delivered': '#228B22',
            'cancelled': '#DC143C',
            'refunded': '#8B008B'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#808080'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_status_badge(self, obj):
        """Display payment status with color coding"""
        colors = {
            'pending': '#FFA500',
            'processing': '#4169E1',
            'completed': '#228B22',
            'failed': '#DC143C',
            'refunded': '#8B008B'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.payment_status, '#808080'),
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment Status'

    def total_display(self, obj):
        """Display total with currency symbol"""
        return format_html(
            '<span style="font-weight: bold; font-size: 1.1em;">${}</span>',
            obj.total
        )
    total_display.short_description = 'Total'

    actions = ['mark_as_confirmed']

    def mark_as_confirmed(self, request, queryset):
        """Bulk action to confirm orders"""
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed')
    mark_as_confirmed.short_description = 'Mark selected orders as confirmed'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem – quantity removed, order field editable"""
    list_display = [
        'id', 'get_order_number', 'item_name', 'item_type',
        'unit_price', 'total_price'
    ]
    list_filter = ['item_type', 'created_at']
    search_fields = ['item_name', 'order__order_number']
    readonly_fields = ['total_price', 'created_at']  # order ko hata diya
    # fields = ['order', 'item_name', 'item_type', 'unit_price', 'custom_requirements']  # optional, agar specific order chahiye

    def get_order_number(self, obj):
        """Display order number with link"""
        if obj.order:
            url = reverse('admin:order_order_change', args=[obj.order.id])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return "-"
    get_order_number.short_description = 'Order'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment (unchanged)"""
    list_display = [
        'payment_id', 'get_order_number', 'amount', 'currency',
        'payment_method', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'payment_gateway', 'created_at']
    search_fields = ['payment_id', 'transaction_id', 'order__order_number']
    readonly_fields = [
        'payment_id', 'transaction_id', 'payment_gateway',
        'card_last4', 'card_brand', 'gateway_response',
        'created_at', 'updated_at', 'completed_at'
    ]

    fieldsets = (
        ('Payment Information', {
            'fields': (
                'order', 'payment_id', 'amount', 'currency',
                'payment_method', 'status'
            )
        }),
        ('Transaction Details', {
            'fields': (
                'transaction_id', 'payment_gateway',
                'card_last4', 'card_brand'
            )
        }),
        ('Gateway Response', {
            'fields': ('gateway_response', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )

    def get_order_number(self, obj):
        """Display order number with link"""
        url = reverse('admin:order_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    get_order_number.short_description = 'Order'

    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#FFA500',
            'processing': '#4169E1',
            'completed': '#228B22',
            'failed': '#DC143C',
            'refunded': '#8B008B'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#808080'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """Admin interface for OrderStatusHistory (unchanged)"""
    list_display = [
        'get_order_number', 'old_status', 'new_status',
        'changed_by', 'created_at'
    ]
    list_filter = ['old_status', 'new_status', 'created_at']
    search_fields = ['order__order_number', 'notes']
    readonly_fields = ['order', 'old_status', 'new_status', 'changed_by', 'created_at']

    def get_order_number(self, obj):
        """Display order number with link"""
        url = reverse('admin:orders_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    get_order_number.short_description = 'Order'