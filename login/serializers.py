from django.forms import ValidationError
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  force_str
from django.utils.http import urlsafe_base64_decode

CustomUser = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': []},
        }

    def validate_email(self, value):
        """
        Validates the email
        """
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('User with this email already exists.')
        return value

    def create(self, validated_data):
        """
        Creates a new user
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.CharField(read_only=True)

    def validate(self, data):
        """
        Validates the login data
        """
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid login credentials.')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified.')

        tokens = user.tokens()

        return {
            'email': user.email,
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }
    
class RequestPasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()

    class Meta:
        fields=['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6, write_only=True)
    token=serializers.CharField(min_length=1, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password', 'token', 'uidb64']

    def validate(self, attrs):
        """
        Validates the data
        """
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            id=force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)