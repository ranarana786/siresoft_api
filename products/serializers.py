from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'          # includes all model fields
        read_only_fields = ['created_at', 'updated_at']   # timestamps read-only