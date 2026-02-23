"""
Django Admin Configuration for Service Management
================================================
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'service_type', 'base_price', 'pricing_model',
        'is_active', 'is_featured', 'display_order'
    ]
    list_filter = [
        'is_active', 'is_featured', 'service_type', 'category', 
        'pricing_model', 'created_at'
    ]
    search_fields = ['name', 'short_description', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'service_type')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description', 'features', 'requirements')
        }),
        ('Visual Elements', {
            'fields': ('icon', 'thumbnail', 'banner_image', 'gallery_images'),
            'classes': ('collapse',)
        }),
        ('Pricing', {
            'fields': ('base_price', 'currency', 'pricing_model')
        }),
        ('Delivery Information', {
            'fields': ('delivery_time', 'delivery_unit', 'revisions_included')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')    