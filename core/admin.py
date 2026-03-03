from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ["id","name","email","subject_short","status_badge","phone_number","created_at"]
    list_filter   = ["status", "created_at"]
    search_fields = ["name", "email"]
    ordering      = ["-created_at"]
    list_per_page = 25
    fieldsets = (
        ("User Message", {"fields": ("name","email","phone_number","subject","message")}),
        ("Admin Actions",   {"fields": ("status","admin_notes")}),
    )
    actions = ["mark_as_read","mark_as_resolved","mark_as_spam"]

    @admin.action(description="Read mark")
    def mark_as_read(self, request, queryset):
        n = queryset.update(status=ContactMessage.Status.READ)
        self.message_user(request, f"{n} message(s) Read marked ")

    @admin.action(description="Resolved mark")
    def mark_as_resolved(self, request, queryset):
        n = queryset.update(status=ContactMessage.Status.RESOLVED)
        self.message_user(request, f"{n} message(s) Resolved marked")

    @admin.action(description="Spam mark")
    def mark_as_spam(self, request, queryset):
        n = queryset.update(status=ContactMessage.Status.SPAM)
        self.message_user(request, f"{n} message(s) Spam marked.")

    @admin.display(description="Subject")
    def subject_short(self, obj):
        return obj.subject[:50] + "..." if len(obj.subject) > 50 else obj.subject

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {"pending": "#f59e0b", "read": "#3b82f6", "resolved": "#10b981", "spam": "#ef4444"}
        color = colors.get(obj.status, "#6b7280")
        return format_html(
            "<span style=\"background:{};color:white;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:bold;\">{}</span>",
            color, obj.get_status_display(),
        )