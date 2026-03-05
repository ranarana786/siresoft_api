from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    # List display columns
    list_display = (
        'name', 'category', 'base_price', 'currency', 'stock',
        'is_active', 'is_featured', 'is_popular', 'display_order', 'created_at'
    )
    list_filter = ('category', 'is_active', 'is_featured', 'is_popular', 'currency')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    # Fieldsets for better organization
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('image', 'banner_image', 'gallery_images'),
            'classes': ('wide',)
        }),
        ('Pricing & Inventory', {
            'fields': ('base_price', 'currency', 'stock'),
            'classes': ('wide',)
        }),
        ('Features', {
            'fields': ('features',),
            'classes': ('wide',)
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'is_popular', 'is_featured', 'display_order'),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Add thumbnail preview for images
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image Preview"

    # Custom actions
    actions = ['make_active', 'make_inactive', 'make_featured', 'make_not_featured']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected products as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected products as inactive"

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected products as featured"

    def make_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
    make_not_featured.short_description = "Mark selected products as not featured"

    # List per page
    list_per_page = 25

admin.site.register(Product, ProductAdmin)