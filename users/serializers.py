from rest_framework import serializers
# from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from .models import Profile, Address

User = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = "__all__"
        exclude = ['profile']

# profile serializer        
class ProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = Profile
        # fields = "__all__"
        exclude = ['user']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]
        read_only_fields = fields

class CurrentUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "phone",
            "profile",
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)

        # -------------------
        #  Update User
        # -------------------
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # -------------------
        #  Update Profile
        # -------------------
        if profile_data:
            addresses_data = profile_data.pop("addresses", [])

            profile = instance.profile

            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

            # -------------------
            # Update Addresses
            # -------------------

        if addresses_data:
            first_address = profile.addresses.first()

            if first_address:
                for attr, value in addresses_data[0].items():
                    setattr(first_address, attr, value)
                first_address.save()
            else:
                Address.objects.create(profile=profile, **addresses_data[0])

        return instance
    
       

       
