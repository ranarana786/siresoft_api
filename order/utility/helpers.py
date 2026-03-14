from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(order, user_email, user_name):
    """
    Send order confirmation email to customer
    """
    try:
        # Email subject
        subject = f"Order Confirmation - #{order.order_number}"
        
        # Email context for template
        context = {
            'order': order,
            'user_name': user_name,
            'order_number': order.order_number,
            'order_date': order.created_at.strftime("%B %d, %Y"),
            'total': order.total,
            'items': order.items.all(),
            'site_url': settings.SITE_URL,
            'support_email': settings.SUPPORT_EMAIL or 'support@example.com'
        }
        
        # Render HTML email
        html_message = render_to_string('emails/order_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Order confirmation email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

