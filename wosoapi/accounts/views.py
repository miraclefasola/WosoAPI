from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from accounts.serializers import UserSerializer, ResendVerificationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from accounts.email import send_verification_email
from accounts.admin_task import delete_unverified_users
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()


# Create your views here.
class APIRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email(user)
        data = serializer.data
        data["SUCCESS"] = "Now proceed to verify your email"
        return Response(data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):

        # str_uid= request.query_param("uid")
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(User, pk=uid)
        # token = request.query_param.get("token")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, "emails/verify_success.html", {"user": user})
        else:
            return render(
                request,
                "emails/verify_failed.html",
                {"message": "Invalid or expired token."},
            )


class DeleteinActiveUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):

        deleted_count, _ = delete_unverified_users()

        return Response(
            {"message": f"Successfully deleted {deleted_count} unverified users."},
            status=status.HTTP_200_OK,
        )


class ResendVerificationView(APIView):
    serializer_class = ResendVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        send_verification_email(user)

        return Response(
            {"success": "Check your email to verify your account."},
            status=status.HTTP_200_OK,
        )
