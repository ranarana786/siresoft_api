"""
Cart URLs Configuration
Add these to your main urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router
router = DefaultRouter()
router.register(r'', views.CartViewSet, basename='cart')

app_name = 'cart'

urlpatterns = [
    path('', include(router.urls)),
]

"""
=============================================================================
AVAILABLE CART ENDPOINTS
=============================================================================

GET     /api/cart/                  # Get complete cart
POST    /api/cart/add/              # Add item to cart
PATCH   /api/cart/update/{id}/      # Update item quantity
DELETE  /api/cart/remove/{id}/      # Remove item
POST    /api/cart/clear/            # Clear cart
GET     /api/cart/summary/          # Cart summary (count + total)
GET     /api/cart/count/            # Just item count

=============================================================================
REQUEST EXAMPLES
=============================================================================

1. ADD TO CART
--------------
POST /api/cart/add/
{
    "item_type": "product",
    "item_id": 1,
    "quantity": 2
}

Response:
{
    "success": true,
    "message": "Product Name added to cart",
    "cart": { ... }
}

2. ADD SERVICE WITH REQUIREMENTS
---------------------------------
POST /api/cart/add/
{
    "item_type": "service",
    "item_id": 5,
    "quantity": 1,
    "custom_requirements": "Need Salesforce integration"
}

3. UPDATE QUANTITY
------------------
PATCH /api/cart/update/3/
{
    "quantity": 5
}

4. REMOVE ITEM
--------------
DELETE /api/cart/remove/3/

5. GET CART
-----------
GET /api/cart/

Response:
{
    "id": 1,
    "items": [
        {
            "id": 1,
            "item_name": "Product Name",
            "item_type": "product",
            "quantity": 2,
            "unit_price": "99.99",
            "total_price": "199.98"
        }
    ],
    "total_price": "199.98",
    "total_items": 2
}

6. GET SUMMARY (for header badge)
----------------------------------
GET /api/cart/summary/

Response:
{
    "id": 1,
    "count": 3,
    "total": "299.97"
}

=============================================================================
"""