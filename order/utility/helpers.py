from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

def send_account_creation_email(user, activation_link):
    """
    Send account creation email with activation link
    """
    try:
        subject = "Welcome! Your Account Has Been Created"
        
        context = {
            'user': user,
            'activation_link': activation_link,
            'site_url': settings.SITE_URL,
            'support_email': settings.SUPPORT_EMAIL or 'support@example.com',
            'login_url': f"{settings.FRONTEND_URL}/login",
        }
        
        html_message = render_to_string('emails/account_creation.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        admin_email = settings.EMAIL_HOST_USER
        if admin_email:
            send_mail(
                subject=f"[NEW USER] {user.email} registered",
                message=f"New user registered: {user.email}\nName: {user.get_full_name()}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                fail_silently=False,
            )
        
        print(f"Account creation email sent to {user.email}")
        return True
        
    except Exception as e:
        print(f"Failed to send account creation email: {str(e)}")
        return False    



def send_order_confirmation_email(order, user_email, user_name):
    """
    Send order confirmation email to customer
    """
    try:
        subject = f"Order Confirmation - #{order.order_number}"
    
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
        
        html_message = render_to_string('emails/order_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        host_email = settings.EMAIL_HOST_USER
        if host_email:
            send_mail(
                subject=f"[NEW ORDER] {subject}",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[host_email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Order copy email sent to host: {host_email}")
        
        print(f"Order confirmation email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

