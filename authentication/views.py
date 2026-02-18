# users/views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer
from django.db import transaction, IntegrityError
from .serializer import LoginSerializer
from drf_spectacular.utils import extend_schema

class RegisterAPIView(APIView):
    
    permission_classes = [AllowAny] 
    
    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegisterSerializer},
    )
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
            except IntegrityError:
                return Response(
                    {"email": "Email already registered."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "message": "User registered successfully.",
                    "user": {
                        "id": str(user.id),
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    
    permission_classes = [AllowAny] 
    
    @extend_schema(
        request=LoginSerializer,
    )
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access = serializer.validated_data['access']
        refresh = serializer.validated_data['refresh']

        return Response({
            "message": "Login successful",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "tokens": {
                "access": access,
                "refresh": refresh
            }
        }, status=status.HTTP_200_OK)