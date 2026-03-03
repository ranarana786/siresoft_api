# contact/emails.py

import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

# Email jahan notification jayegi
ADMIN_NOTIFICATION_EMAIL = "muhammadawais9868@gmail.com"


def send_contact_notification(contact_message):

    subject = f"[New Contact] {contact_message.subject} — {contact_message.name}"

    # ── HTML Email Body ──────────────────────────────────────────
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Message</title>
    </head>
    <body style="margin:0;padding:0;background-color:#f4f6f9;font-family:'Segoe UI',Arial,sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0"
               style="background-color:#f4f6f9;padding:40px 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0"
                           style="max-width:600px;width:100%;background:#ffffff;
                                  border-radius:12px;overflow:hidden;
                                  box-shadow:0 4px 20px rgba(0,0,0,0.08);">

                        <!-- Header -->
                        <tr>
                            <td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
                                       padding:40px 40px 35px;text-align:center;">
                                <h1 style="margin:0;color:#ffffff;font-size:26px;
                                           font-weight:700;letter-spacing:0.5px;">
                                    📬 New Contact Message
                                </h1>
                                <p style="margin:10px 0 0;color:#a8b8d8;font-size:14px;">
                                    Someone reached out via the contact form
                                </p>
                            </td>
                        </tr>

                        <!-- Alert Banner -->
                        <tr>
                            <td style="background:#e8f4fd;padding:14px 40px;
                                       border-left:4px solid #3b82f6;">
                                <p style="margin:0;color:#1e40af;font-size:14px;font-weight:500;">
                                    🕐 Received on:
                                    <strong>
                                        {contact_message.created_at.strftime("%B %d, %Y at %I:%M %p UTC")}
                                    </strong>
                                </p>
                            </td>
                        </tr>

                        <!-- Sender Info -->
                        <tr>
                            <td style="padding:35px 40px 20px;">
                                <h2 style="margin:0 0 20px;color:#1a1a2e;font-size:16px;
                                           font-weight:600;text-transform:uppercase;
                                           letter-spacing:1px;border-bottom:2px solid #f0f0f0;
                                           padding-bottom:12px;">
                                    Sender Information
                                </h2>

                                <!-- Name -->
                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="margin-bottom:14px;">
                                    <tr>
                                        <td width="130" style="color:#6b7280;font-size:13px;
                                                               font-weight:600;vertical-align:top;
                                                               padding-top:2px;">
                                            👤 Full Name
                                        </td>
                                        <td style="color:#1a1a2e;font-size:15px;font-weight:500;">
                                            {contact_message.name}
                                        </td>
                                    </tr>
                                </table>

                                <!-- Email -->
                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="margin-bottom:14px;">
                                    <tr>
                                        <td width="130" style="color:#6b7280;font-size:13px;
                                                               font-weight:600;vertical-align:top;
                                                               padding-top:2px;">
                                            📧 Email
                                        </td>
                                        <td>
                                            <a href="mailto:{contact_message.email}"
                                               style="color:#3b82f6;font-size:15px;
                                                      text-decoration:none;font-weight:500;">
                                                {contact_message.email}
                                            </a>
                                        </td>
                                    </tr>
                                </table>

                                <!-- Phone -->
                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="margin-bottom:14px;">
                                    <tr>
                                        <td width="130" style="color:#6b7280;font-size:13px;
                                                               font-weight:600;vertical-align:top;
                                                               padding-top:2px;">
                                            📞 Phone
                                        </td>
                                        <td style="color:#1a1a2e;font-size:15px;font-weight:500;">
                                            {contact_message.phone_number if contact_message.phone_number else
                                             '<span style="color:#9ca3af;font-style:italic;">Not provided</span>'}
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- Subject -->
                        <tr>
                            <td style="padding:0 40px 20px;">
                                <h2 style="margin:0 0 12px;color:#1a1a2e;font-size:16px;
                                           font-weight:600;text-transform:uppercase;
                                           letter-spacing:1px;border-bottom:2px solid #f0f0f0;
                                           padding-bottom:12px;">
                                    Subject
                                </h2>
                                <div style="background:#f8fafc;border-radius:8px;
                                            padding:14px 18px;border-left:3px solid #0f3460;">
                                    <p style="margin:0;color:#1a1a2e;font-size:15px;font-weight:600;">
                                        {contact_message.subject}
                                    </p>
                                </div>
                            </td>
                        </tr>

                        <!-- Message -->
                        <tr>
                            <td style="padding:0 40px 35px;">
                                <h2 style="margin:0 0 12px;color:#1a1a2e;font-size:16px;
                                           font-weight:600;text-transform:uppercase;
                                           letter-spacing:1px;border-bottom:2px solid #f0f0f0;
                                           padding-bottom:12px;">
                                    Message
                                </h2>
                                <div style="background:#f8fafc;border-radius:8px;
                                            padding:20px 18px;border-left:3px solid #10b981;
                                            line-height:1.7;">
                                    <p style="margin:0;color:#374151;font-size:15px;
                                              white-space:pre-wrap;">
                                        {contact_message.message}
                                    </p>
                                </div>
                            </td>
                        </tr>

                        <!-- CTA Button -->
                        <tr>
                            <td style="padding:0 40px 35px;text-align:center;">
                                <a href="mailto:{contact_message.email}?subject=Re: {contact_message.subject}"
                                   style="display:inline-block;background:linear-gradient(135deg,#0f3460,#1a1a2e);
                                          color:#ffffff;text-decoration:none;padding:14px 32px;
                                          border-radius:8px;font-size:15px;font-weight:600;
                                          letter-spacing:0.3px;">
                                    Reply to {contact_message.name} →
                                </a>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background:#f8fafc;padding:20px 40px;
                                       border-top:1px solid #e5e7eb;text-align:center;">
                                <p style="margin:0;color:#9ca3af;font-size:12px;line-height:1.6;">
                                    This is an automated notification from your website's contact form.<br>
                                    Please do not reply directly to this email.
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    # Plain text fallback
    text_content = f"""
NEW CONTACT MESSAGE
===================

Received: {contact_message.created_at.strftime("%B %d, %Y at %I:%M %p UTC")}

SENDER INFO
-----------
Name    : {contact_message.name}
Email   : {contact_message.email}
Phone   : {contact_message.phone_number or "Not provided"}

SUBJECT
-------
{contact_message.subject}

MESSAGE
-------
{contact_message.message}

---
Reply directly: {contact_message.email}
    """.strip()

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,                    # Plain text (fallback)
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[ADMIN_NOTIFICATION_EMAIL],
            reply_to=[contact_message.email],     # Reply to user
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        logger.info(
            "Contact notification sent to %s for message id=%s",
            ADMIN_NOTIFICATION_EMAIL,
            contact_message.id,
        )
        return True

    except Exception as exc:
        logger.error(
            "Failed to send contact notification for id=%s: %s",
            contact_message.id,
            exc,
        )
        return False