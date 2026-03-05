# pricing/serializers.py
"""
Serializers for Pricing Plans API
"""

from rest_framework import serializers
from .models import PricingPlan, PlanFeature, PlanComparisonValue, PlanComparison


class PlanFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for plan features
    """
    class Meta:
        model = PlanFeature
        fields = ['id', 'name', 'is_included', 'order']


class PricingPlanSerializer(serializers.ModelSerializer):
    """
    Complete serializer for pricing plans with features
    """
    features = PlanFeatureSerializer(many=True, read_only=True)
    
    # Separate included/excluded features for easier frontend use
    included_features = serializers.SerializerMethodField()
    excluded_features = serializers.SerializerMethodField()
    
    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'slug', 'plan_type', 'tagline',
            'price', 'billing_period',
            'is_featured', 'is_popular', 'badge_text', 'button_text',
            'is_active', 'order',
            'features', 'included_features', 'excluded_features',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_included_features(self, obj):
        """Get only included features"""
        features = obj.features.filter(is_included=True).order_by('order')
        return [f.name for f in features]
    
    def get_excluded_features(self, obj):
        """Get only excluded features"""
        features = obj.features.filter(is_included=False).order_by('order')
        return [f.name for f in features]


class PricingPlanListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing plans (without features)
    """
    features = PlanFeatureSerializer(many=True, read_only=True)
    features_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'slug', 'plan_type', 'tagline',
            'price', 'billing_period','features',
            'is_featured', 'is_popular', 'badge_text', 'button_text',
            'features_count', 'order'
        ]
    
    def get_features_count(self, obj):
        """Count of included features"""
        return obj.features.filter(is_included=True).count()
    
class PlanComparisonValueSerializer(serializers.ModelSerializer):
    plan_id = serializers.IntegerField(source="plan.id", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = PlanComparisonValue
        fields = [
            "id",
            "plan_id",
            "plan_name",
            "value",
            "is_available",
        ]
        
class PlanComparisonSerializer(serializers.ModelSerializer):
    values = PlanComparisonValueSerializer(many=True, read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = PlanComparison
        fields = [
            "id",
            "name",
            "category",
            "description",
            "order",
            "service_name",
            "values",   # 👈 important for table
        ]        