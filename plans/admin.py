# pricing/admin.py
"""
Django Admin Configuration for Pricing Plans
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import PricingPlan, PlanFeature


class PlanFeatureInline(admin.TabularInline):
    """
    Inline editor for plan features
    """
    model = PlanFeature
    extra = 1
    fields = ['name', 'is_included', 'order']
    ordering = ['order']


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for Pricing Plans
    """
    list_display = [
        'name', 'plan_type', 'price_display', 'billing_period',
        'is_featured', 'is_popular', 'is_active', 'order'
    ]
    list_filter = ['plan_type', 'billing_period', 'is_featured', 'is_popular', 'is_active']
    search_fields = ['name', 'tagline']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'price']
    
    inlines = [PlanFeatureInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'plan_type', 'tagline')
        }),
        ('Pricing', {
            'fields': ('price', 'billing_period')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_popular', 'badge_text', 'button_text', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def price_display(self, obj):
        """Display formatted price"""
        return format_html(
            '<span style="font-weight: bold; color: #0066ff;">${}</span> / {}',
            obj.price, obj.billing_period
        )
    price_display.short_description = 'Price'
    
    actions = ['activate_plans', 'deactivate_plans', 'mark_featured', 'mark_popular']
    
    def activate_plans(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} plan(s) activated.')
    activate_plans.short_description = 'Activate selected plans'
    
    def deactivate_plans(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} plan(s) deactivated.')
    deactivate_plans.short_description = 'Deactivate selected plans'
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} plan(s) marked as featured.')
    mark_featured.short_description = 'Mark as featured'
    
    def mark_popular(self, request, queryset):
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'{updated} plan(s) marked as popular.')
    mark_popular.short_description = 'Mark as popular'


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    """
    Admin interface for Plan Features
    """
    list_display = ['name', 'plan', 'is_included_display', 'order']
    list_filter = ['plan', 'is_included']
    search_fields = ['name', 'plan__name']
    ordering = ['plan', 'order']
    
    def is_included_display(self, obj):
        """Display feature status with icon"""
        if obj.is_included:
            return format_html(
                '<span style="color: #00a651; font-size: 16px;">✓</span> Included'
            )
        return format_html(
            '<span style="color: #e74c3c; font-size: 16px;">✗</span> Not Included'
        )
    is_included_display.short_description = 'Status'