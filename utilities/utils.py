from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

def validate_strong_password(password):
    try:
        validate_password(password)
    except ValidationError as e:
        raise serializers.ValidationError(list(e.messages))