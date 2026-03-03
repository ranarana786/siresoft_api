from django.db import models
from django.core.validators import RegexValidator


class ContactMessage(models.Model):
    """
    Contact Us form submitted data.
    """

    class Status(models.TextChoices):
        PENDING  = "pending",  "Pending"
        READ     = "read",     "Read"
        RESOLVED = "resolved", "Resolved"
        SPAM     = "spam",     "Spam"

    # ---- User submitted fields ----------------------------------
    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        default="",
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Enter Valid Phone Number, e.g. +923001234567",
            )
        ],
    )

    subject = models.CharField(max_length=255)

    message = models.TextField()

    # ---- Admin / tracking fields --------------------------------
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    admin_notes = models.TextField(
        blank=True,
        default="",
        help_text="Internal notes -- only admin can see",
    )

    # For spam tracking
    # ip_address = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering            = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.subject} -- {self.email}"