from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("register/", APIRegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/delete/", DeleteinActiveUsers.as_view(), name="admin_delete"),
    path(
        "verify/<str:uid>/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path("resend/verify", ResendVerificationView.as_view(), name="resend_verification"),
]
