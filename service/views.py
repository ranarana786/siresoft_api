from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ServiceCategory, Service
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from .serializers import ServiceCategorySerializer
from .serializers import (
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceWriteSerializer,
)



class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    Enterprise-level Service Category API
    """
    serializer_class = ServiceCategorySerializer
    queryset = ServiceCategory.objects.all()
    lookup_field = "slug"
    
    parser_classes = [MultiPartParser, FormParser]  # important for multipart

    # Swagger documentation
    @extend_schema(
        request=ServiceCategorySerializer,
        responses=ServiceCategorySerializer
    )
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    lookup_field = "slug"
   

    # def get_queryset(self):
    #     """
    #     Public users only see active services.
    #     Admin/staff see all.
    #     """
    #     user = self.request.user
    #     if user.is_authenticated and user.is_staff:
    #         return Service.objects.all()
    #     return Service.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceListSerializer
        elif self.action == "retrieve":
            return ServiceDetailSerializer
        return ServiceWriteSerializer
    
# from rest_framework.viewsets import ReadOnlyModelViewSet

# class ServiceViewSet(ReadOnlyModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceListSerializer            