from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


def send_verification_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    subject = f"Verify your account with us, {user.username}"
    from_email = "shetalksfooty@gmail.com"
    to = user.email

    verify_url = f"https://wosoapi.onrender.com/verify/{uid}/{token}/"


    # Render HTML template
    html_content = render_to_string(
        "emails/verify_email.html", {"user": user, "verification_link": verify_url}
    )

    # Plain text fallback
    text_content = f"Hi {user.username}, please verify your account: {verify_url}"

    # Create and send email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # <-- goes into plain text body
        from_email=from_email,
        to=[to],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
