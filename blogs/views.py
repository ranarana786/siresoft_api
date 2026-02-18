from rest_framework import viewsets, permissions
from .models import Blog, Category
from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer,
    CategorySerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BlogViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Blog.objects.select_related('author', 'category')

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        return BlogDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
