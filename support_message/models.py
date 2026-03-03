from django.db import models


class SupportMessage(models.Model):
    """
    Stores every message submitted via the Contact / Support popup.
    """
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, default="")
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Support Message"
        verbose_name_plural = "Support Messages"

    def __str__(self):
        return f"[{self.status.upper()}] {self.name} — {self.subject or 'No Subject'}"