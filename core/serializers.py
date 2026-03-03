from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "subject",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long."
            )
        return value

    def validate_subject(self, value):
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError(
                "Subject must be at least 5 characters long."
            )
        return value

    def validate_message(self, value):
        value = value.strip()
        if len(value) < 20:
            raise serializers.ValidationError(
                "Message must be at least 20 characters long."
            )
        if len(value) > 5000:
            raise serializers.ValidationError(
                "Message cannot exceed 5000 characters."
            )
        return value

    def validate_phone_number(self, value):
        return value.strip() if value else value