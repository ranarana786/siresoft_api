from django.contrib import admin
from .models import SupportMessage


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Sender Info", {"fields": ("name", "email")}),
        ("Message", {"fields": ("subject", "message")}),
        ("Status & Timestamps", {"fields": ("status", "created_at", "updated_at")}),
    )