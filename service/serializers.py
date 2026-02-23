from rest_framework import serializers
from django.utils.text import slugify
from .models import ServiceCategory,Service


class ServiceCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for ServiceCategory model.
    Designed using industry best practices.
    """

    slug = serializers.SlugField(
        read_only=True
    )

    class Meta:
        model = ServiceCategory
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "display_order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    # -------------------------
    # Field Level Validation
    # -------------------------
    def validate_name(self, value):
        """
        Ensure name is properly formatted and trimmed.
        """
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Category name must be at least 2 characters long."
            )

        return value

    # -------------------------
    # Object Level Validation
    # -------------------------
    def validate(self, attrs):
        """
        Additional cross-field validation if needed in future.
        """
        return attrs

    # -------------------------
    # Create Override (Optional)
    # -------------------------
    def create(self, validated_data):
        """
        Explicit create method (future-proofing for scaling).
        """
        return ServiceCategory.objects.create(**validated_data)

    # -------------------------
    # Update Override (Optional)
    # -------------------------
    def update(self, instance, validated_data):
        """
        Explicit update for better maintainability.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
# -----------------------------
# Base Serializer
# -----------------------------
class BaseServiceSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "service_type",
            "short_description",
            "description",
            "features",
            "requirements",
            "icon",
            "thumbnail",
            "banner_image",
            "gallery_images",
            "base_price",
            "currency",
            "pricing_model",
            "delivery_time",
            "delivery_unit",
            "revisions_included",
            "is_active",
            "is_featured",
            "display_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


# -----------------------------
# List Serializer (Lightweight)
# -----------------------------
class ServiceListSerializer(BaseServiceSerializer):
    category = ServiceCategorySerializer(read_only=True) 
    class Meta(BaseServiceSerializer.Meta):
        fields = '__all__'


# -----------------------------
# Detail Serializer
# -----------------------------
class ServiceDetailSerializer(BaseServiceSerializer):
    pass


# # -----------------------------
# # Create/Update Serializer
# # -----------------------------
class ServiceWriteSerializer(BaseServiceSerializer):
    pass    