from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Address, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    
class AddressInline(admin.TabularInline):
    model = Address
    extra = 0    


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "phone",
        "date_joined",
        "get_country",
    )

    ordering = ("-date_joined",)
    search_fields = ("email", "first_name", "last_name")

    readonly_fields = (
    "get_country",
    "get_address",
    "get_city",
    "get_state",
    "get_postal_code",
)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        
        ("Personal Info", {"fields": ("first_name", "last_name", "phone")}),
        
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
        
        ("Profile Info", {"fields": ("get_country", "get_city",
                                     "get_state", "get_postal_code", 
                                     "get_address")}),
        )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff"),
        }),
    )

    def get_country(self, obj):
        if hasattr(obj, "profile"):
            address = obj.profile.addresses.first()
            return address.country if address else "No country"
        return "No profile"
    get_country.short_description = "Country"

    def get_address(self, obj):
        if hasattr(obj, "profile"):
            address = obj.profile.addresses.first()
            return address.address if address else "No address"
        return "No profile"
    get_address.short_description = "Address"
    
    def get_city(self, obj):
        if hasattr(obj, "profile"):
            address = obj.profile.addresses.first()
            return address.city if address else "No city"
        return "No profile"
    get_city.short_description = "City"
    
    def get_state(self, obj):
        if hasattr(obj, "profile"):
            address = obj.profile.addresses.first()
            return address.state if address else "No state"
        return "No profile"
    get_state.short_description = "State"
    
    def get_postal_code(self, obj):
        if hasattr(obj, "profile"):
            address = obj.profile.addresses.first()
            return address.postal_code if address else "No postal-code"
        return "No profile"
    get_postal_code.short_description = "Postal Code"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [AddressInline]
    list_display = ('user',)
    readonly_fields = ('user',)
    
@admin.register(Address)    
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'profile', 
        'country',
        'city', 
        'state', 
        'postal_code'
        ]
    list_filter = ['country', 'city', 'state', 'postal_code']