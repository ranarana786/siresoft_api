"""
Order and Payment URLs Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
# router.register(r'order_items', OrderItemViewset, basename='order-items')
router.register(r'', OrderViewSet, basename='orders')



app_name = 'orders'

urlpatterns = [
    path('', include(router.urls)),
]