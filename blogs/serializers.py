from rest_framework import serializers
from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BlogListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'author',
            'category',
            'created_at',
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = '__all__'
