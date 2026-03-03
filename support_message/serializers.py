from rest_framework import serializers
from .models import SupportMessage


class SupportMessageSerializer(serializers.ModelSerializer):
    """
    Validates and serializes the contact/support form payload.
    """

    class Meta:
        model = SupportMessage
        fields = ["id", "name", "email", "subject", "message", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    # ── Custom validation ─────────────────────────────────────────────────────

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters.")
        return value.strip()