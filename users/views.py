from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer, CurrentUserSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]
    
class CurrentUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CurrentUserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # request.user ko return kar raha hai
        return self.request.user    


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        request=ProfileSerializer,
    )

    def get_object(self):
        return self.request.user.profile
    
