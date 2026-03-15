from collections import defaultdict

from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.generics import ListAPIView
from django.db.models import Prefetch

from .models import (PricingPlan, PlanFeature, 
                     PlanComparison, PlanComparisonValue)
from .serializers import (
    PricingPlanSerializer,
    PricingPlanListSerializer,
    PlanFeatureSerializer,
    PlanComparisonSerializer,PlanComparisonValueSerializer
)

# Create your views here.
class PlanFeatureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Plan Features (Admin only)
    """
    queryset = PlanFeature.objects.select_related('plan')
    serializer_class = PlanFeatureSerializer


# class ActivePlanFeaturesAPIView(ListAPIView):
#     serializer_class = PlanFeatureSerializer

#     def get_queryset(self):
#         return PlanFeature.objects.filter(
#             is_included=True,
#         ) 

class PricingPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pricing Plans
    
    list: Get all active pricing plans
    retrieve: Get specific plan details with features
    create: Create new plan (admin only)
    update: Update plan (admin only)
    destroy: Delete plan (admin only)
    
    Custom Actions:
    - featured: Get featured plans
    - popular: Get popular/recommended plans
    """
    queryset = PricingPlan.objects.prefetch_related('features')
    lookup_field = 'slug'
    
    def get_queryset(self):
        """
        Return only active plans for regular users
        Admins can see all plans
        """
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_active=True)
    
    def get_serializer_class(self):
        """
        Use list serializer for list view, detail for others
        """
        if self.action == 'list':
            return PricingPlanListSerializer
        return PricingPlanSerializer
    
    def get_permissions(self):
        """
        Allow anyone to view plans
        Only admins can create/update/delete
        """
        if self.action in ['list', 'retrieve', 'featured', 'popular']:
            return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured/recommended plans
        URL: /api/pricing-plans/featured/
        """
        plans = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular plans
        URL: /api/pricing-plans/popular/
        """
        plans = self.get_queryset().filter(is_popular=True)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)

class PlanComparisonTableView(ListAPIView):
    serializer_class = PlanComparisonSerializer

    def get(self, request):
        queryset = (
            PlanComparison.objects
            .filter(is_active=True)
            .prefetch_related("values__plan", "service")
            .order_by("order")
        )

        serializer = PlanComparisonSerializer(queryset, many=True)
        data = serializer.data

        grouped = defaultdict(list)

        for item in data:
            service_name = item.pop("service_name")
            
            # convert values list to plan-wise format
            formatted_values = []
            for v in item["values"]:
                formatted_values.append({
                    "plan": v["plan_name"].lower(),
                    "value": v["value"]
                })

            item["values"] = formatted_values
            grouped[service_name].append(item)

        return Response(grouped)