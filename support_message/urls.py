from django.urls import path
from .views import SupportMessageCreateView

urlpatterns = [
    # POST  /api/contact/support/  →  Submit contact / support form
    path("", SupportMessageCreateView.as_view(), name="support-create"),
]