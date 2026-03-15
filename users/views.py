from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer
from .serializers import ProfileSerializer, CurrentUserSerializer, ChangePasswordSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]
    
class CurrentUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        # ✅ Custom response, serializer data not returned
        return Response({
            "success": True,
            "message": "Profile updated successfully",
            "errors": None
        }, status=status.HTTP_200_OK) 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import ChangePasswordSerializer


class ChangePasswordView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        return Response({
            "success": True,
            "message": "Password updated successfully"
        })

    

class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        request=ProfileSerializer,
    )

    def get_object(self):
        return self.request.user.profile
    
