from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanFeatureViewSet, PricingPlanViewSet

# Initialize DRF Router
router = DefaultRouter()
router.register(r'', PricingPlanViewSet, basename='pricing-plan')
router.register(r'plans-feature', PlanFeatureViewSet, basename='plan-feature')

urlpatterns = [
    path("", include(router.urls)),
    # path('features/included/', ActivePlanFeaturesAPIView.as_view(), name='active-features'),
]