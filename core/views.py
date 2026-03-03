import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .email import send_contact_notification

from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


class ContactRateThrottle(AnonRateThrottle):
    """
    Spam prevention: maximum 5 messages per hour per IP address.

    Add this in settings.py:
        REST_FRAMEWORK = {
            "DEFAULT_THROTTLE_RATES": {
                "contact": "5/hour",
            }
        }
    """
    scope = "contact"


def _get_client_ip(request):
    """Retrieve the real client IP address (works behind proxies as well)."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class ContactMessageCreateView(APIView):
    """
    POST /api/contact/

    Authentication : Not required (public endpoint)
    Throttle       : 5 requests per hour per IP address
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "There are errors in the submitted form. Please review and try again.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        contact_msg = serializer.save()

        logger.info(
            "New contact message | name=%s email=%s ip=%s",
            contact_msg.name,
            contact_msg.email,
        )
        
        # ── Send admin notification email ─────────────────────────
        email_sent = send_contact_notification(contact_msg)

        if not email_sent:
            logger.warning(
                "Admin notification email failed for contact id=%s "
                "— message is saved in DB.",
                contact_msg.id,
            )

        return Response(
            {
                "success": True,
                "message": (
                    "Your message has been received successfully. "
                    "We will get back to you as soon as possible."
                ),
                "data": {
                    "id": contact_msg.id,
                    "submitted_at": contact_msg.created_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )