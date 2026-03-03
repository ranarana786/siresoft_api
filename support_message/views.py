from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SupportMessage
from .serializers import SupportMessageSerializer


# ── Target email (where all support messages are delivered) ───────────────────
SUPPORT_EMAIL = "muhammadawais9868@gmail.com"


class SupportMessageCreateView(APIView):
    """
    POST /api/contact/support/
    Accepts the contact form, saves to DB, and sends two emails:
      1. Notification to SUPPORT_EMAIL with full details.
      2. Auto-reply confirmation to the sender.
    """

    def post(self, request):
        serializer = SupportMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ── Save to database ──────────────────────────────────────────────────
        instance = serializer.save()

        # ── Send notification email to support ───────────────────────────────
        try:
            self._send_support_notification(instance)
        except Exception as e:
            # Log but don't fail the whole request
            print(f"[SireSoft] Support notification email failed: {e}")

        # ── Send auto-reply to the user ───────────────────────────────────────
        try:
            self._send_user_confirmation(instance)
        except Exception as e:
            print(f"[SireSoft] User confirmation email failed: {e}")

        return Response(
            {
                "detail": "Your message has been received. We'll get back to you shortly.",
                "id": instance.id,
            },
            status=status.HTTP_201_CREATED,
        )

    # ── Private helpers ───────────────────────────────────────────────────────

    def _send_support_notification(self, instance: SupportMessage):
        subject = (
            f"[SireSoft Support] New message from {instance.name}"
            + (f" — {instance.subject}" if instance.subject else "")
        )

        text_body = f"""
New support message received on SireSoft website.

──────────────────────────────────────
Name    : {instance.name}
Email   : {instance.email}
Subject : {instance.subject or '(none)'}
Date    : {instance.created_at.strftime('%d %b %Y, %I:%M %p')}
──────────────────────────────────────

Message:
{instance.message}

──────────────────────────────────────
Reply directly to this email to respond to {instance.name}.
        """.strip()

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    body {{ font-family: Arial, sans-serif; background: #f4f6fb; margin: 0; padding: 0; }}
    .wrapper {{ max-width: 560px; margin: 32px auto; background: #fff;
                border-radius: 6px; overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
    .header {{ background: linear-gradient(135deg, #0b1957, #1a2f8a);
               padding: 24px 28px; color: #fff; }}
    .header h2 {{ margin: 0; font-size: 20px; font-weight: 700; }}
    .header p  {{ margin: 4px 0 0; font-size: 13px; opacity: .75; }}
    .body   {{ padding: 28px; }}
    .field  {{ margin-bottom: 16px; }}
    .label  {{ font-size: 11px; letter-spacing: .8px; text-transform: uppercase;
               color: #8a93b0; font-weight: 600; margin-bottom: 4px; }}
    .value  {{ font-size: 15px; color: #1a1f3c; font-weight: 500; }}
    .msg-box {{ background: #f7f9ff; border-left: 3px solid #1a2f8a;
                padding: 16px 18px; border-radius: 0 4px 4px 0;
                font-size: 14px; color: #3a4060; line-height: 1.7; white-space: pre-wrap; }}
    .footer {{ padding: 18px 28px; background: #f7f9ff;
               font-size: 12px; color: #8a93b0; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h2>New Support Message</h2>
      <p>Received via SireSoft website contact form</p>
    </div>
    <div class="body">
      <div class="field">
        <div class="label">From</div>
        <div class="value">{instance.name} &lt;{instance.email}&gt;</div>
      </div>
      <div class="field">
        <div class="label">Subject</div>
        <div class="value">{instance.subject or '(No subject)'}</div>
      </div>
      <div class="field">
        <div class="label">Message</div>
        <div class="msg-box">{instance.message}</div>
      </div>
    </div>
    <div class="footer">
      Reply to this email to respond directly to {instance.name}. &nbsp;|&nbsp; SireSoft © 2024
    </div>
  </div>
</body>
</html>
        """.strip()

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[SUPPORT_EMAIL],
            reply_to=[instance.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

    def _send_user_confirmation(self, instance: SupportMessage):
        subject = "We received your message — SireSoft"

        text_body = f"""
Hi {instance.name},

Thank you for contacting SireSoft!

We have received your message and our team will get back to you within 24 hours.

Your message:
"{instance.message}"

Best regards,
SireSoft Support Team
info@siresoft.com | +1-201-762-5042
        """.strip()

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    body {{ font-family: Arial, sans-serif; background: #f4f6fb; margin: 0; padding: 0; }}
    .wrapper {{ max-width: 540px; margin: 32px auto; background: #fff;
                border-radius: 6px; overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
    .header {{ background: linear-gradient(135deg, #0b1957, #1a2f8a);
               padding: 28px; text-align: center; color: #fff; }}
    .header h2 {{ margin: 0 0 6px; font-size: 22px; }}
    .header p  {{ margin: 0; opacity: .75; font-size: 13px; }}
    .body {{ padding: 32px 28px; color: #3a4060; font-size: 15px; line-height: 1.7; }}
    .highlight {{ background: #f7f9ff; border-left: 3px solid #1a2f8a;
                  padding: 14px 18px; border-radius: 0 4px 4px 0;
                  font-style: italic; color: #5a6480; margin: 20px 0; font-size: 14px; }}
    .footer {{ padding: 18px 28px; background: #f7f9ff;
               font-size: 12px; color: #8a93b0; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h2>✓ Message Received</h2>
      <p>SireSoft Support Team</p>
    </div>
    <div class="body">
      <p>Hi <strong>{instance.name}</strong>,</p>
      <p>
        Thank you for reaching out! We have received your message and our team
        will get back to you <strong>within 24 hours</strong>.
      </p>
      <div class="highlight">"{instance.message[:200]}{'...' if len(instance.message) > 200 else ''}"</div>
      <p>
        In the meantime, you can also reach us at:<br />
        📧 info@siresoft.com<br />
        📞 +1-201-762-5042 &nbsp;|&nbsp; +92 313 4324899
      </p>
      <p>Best regards,<br /><strong>SireSoft Support Team</strong></p>
    </div>
    <div class="footer">SireSoft © 2024 &nbsp;|&nbsp; 47609 Glengarry Blvd. Canton, MI. 48188</div>
  </div>
</body>
</html>
        """.strip()

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)