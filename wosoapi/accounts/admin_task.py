from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


def delete_unverified_users(days=7):
    cutoff = timezone.now() - timedelta(days=days)
    if User.objects.filter(is_active=False, date_joined__lt=cutoff).exists():
        User.objects.filter(is_active=False, date_joined__lt=cutoff).delete()
        return "Unverified users deleted successfully."
    else:
        return "No unverified users to delete."