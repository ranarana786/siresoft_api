from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ServiceCategoryViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r"categories", ServiceCategoryViewSet, basename="service-category")
router.register(r"", ServiceViewSet, basename="service")

urlpatterns = [
    path("", include(router.urls)),
]