from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
from utilities.utils import validate_strong_password
from django.db import transaction, IntegrityError

class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles user registration with full validation. 
    """

    password = serializers.CharField(
        write_only=True,       
        required=True,
        min_length=8,
        style={'input_type': 'password'}, 
    )
    confirm_password = serializers.CharField(
        write_only=True,      
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password',
            'confirm_password',
        ]
        read_only_fields = ['id'] 


    def validate_email(self, value):
        normalized = value.lower().strip()
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError(
                "An account Email already exists."
            )

        return normalized

    def validate_first_name(self, value):
        value = value.strip()
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError(
                "First name can only contain alphabetic characters."
            )
        if len(value) < 2:
            raise serializers.ValidationError(
                "First name must be at least 2 characters long."
            )
        return value.title()

    def validate_last_name(self, value):
        value = value.strip()
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError(
                "Last name can only contain alphabetic characters."
            )
        if len(value) < 2:
            raise serializers.ValidationError(
                "Last name must be at least 2 characters long."
            )
        return value.title()

    def validate_password(self, value):
        validate_strong_password(value)
        return value
    
    def validate_phone(self, value):
        """
        validate phone number
        """
        phone = value.strip()

        if not phone.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) < 11 or len(phone) > 15:
            raise serializers.ValidationError(
                "Phone number must be between 11 and 15 digits."
            )

        return phone

    def validate(self, attrs):
        """
        Object-level validator: runs AFTER all field validators.
        Used for validations that need multiple fields at once.
        """
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                "Passwords do not match."
            })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone = validated_data.get('phone', '')
            )
        except IntegrityError:
            raise serializers.ValidationError({"email": "Email already registered."})
        return user
    
class LoginSerializer(serializers.Serializer):
    """
    Handle user Login with full validation
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate_email(self, value):
        return value.lower().strip()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid credentials. Please try again."]
            })
        
        authenticated_user = authenticate(username=email, password=password)        
        if not authenticated_user:
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid credentials. Please try again."]
            }) 
        refresh = RefreshToken.for_user(authenticated_user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        attrs['user'] = authenticated_user
        return attrs    
                   