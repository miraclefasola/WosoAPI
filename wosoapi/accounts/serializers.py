from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.db.models import Q


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm"]

    def validate(self, attrs):
        password1 = attrs["password"]
        password2 = attrs["password_confirm"]
        email_verify = attrs["email"]

        if not email_verify:
            raise serializers.ValidationError({"email": "Email cannot be empty."})
        if password1 != password2:
            raise serializers.ValidationError("Password mismatch")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        email = validated_data.pop("email")

        # user= User.objects.create_user(username=email, password=password )

        # return user

        try:
            user = User.objects.create_user(
                username=email, password=password, email=email
            )
            user.is_active = False
            user.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )

        return user


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(Q(username=value) | Q(email=value))
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Account does not exist, sign up instead."
            )

        if user.is_active:
            raise serializers.ValidationError(
                "This account is already verified. Please log in instead."
            )

        return value
