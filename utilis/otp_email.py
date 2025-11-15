from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone





def send_otp(user,otp):
    context = {
        "otp_code": otp,
        "current_year": timezone.now().year
    }

    html_content = render_to_string("email_otp.html", context)
    email = EmailMultiAlternatives(
        subject="Your OTP Code",
        body=f"Your OTP is {otp}",
        from_email="",
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
