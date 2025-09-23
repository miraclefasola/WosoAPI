from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


def delete_unverified_users(days=7):
    cutoff = timezone.now() - timedelta(days=days)
    queryset = User.objects.filter(is_active=False, date_joined__lt=cutoff)
    if queryset.exists():
        return queryset.delete()
    return (0, {})
