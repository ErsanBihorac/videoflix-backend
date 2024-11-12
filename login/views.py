from rest_framework.response import Response
from rest_framework.views import APIView
from login.serializers import RegisterSerializer, LoginSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status
from django.urls import reverse
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Registers a user and sents a verification email
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user=CustomUser.objects.get(email=user.email)
        token=RefreshToken.for_user(user).access_token
        current_site=get_current_site(request).domain
        relativeLink=reverse('email-verify')
        confirmation_link='http://'+current_site+relativeLink+'?token='+str(token)
        Util.send_registration_email(user, confirmation_link)
        return Response({'message': 'User registered succcessfully!'}, status=status.HTTP_201_CREATED)
    
class LoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        """
        Logs the user in
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = {
            'email': serializer.validated_data['email'],
            'refresh': serializer.validated_data['refresh'],
            'access': serializer.validated_data['access'],
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class VerifyEmailView(generics.GenericAPIView):
    def get(self, request):
        """
        Verifies the user
        """
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user=CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Succesfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class RequestPasswordResetView(generics.GenericAPIView):
    def post(self, request):
        """
        Sends email with which the user can reset their password
        """
        email=request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            user=CustomUser.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            # current_site=get_current_site(request=request).domain
            current_site="https://ersanbihorac.de/Videoflix"
            relativeLink=reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            # production comfirmation link
            confirmation_link='http://'+current_site+relativeLink 
            # development comfirmation link
            # confirmation_link='http://localhost:4200'+relativeLink
            Util.send_reset_password_email(user, confirmation_link)       
        return Response({'success':'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        """
        Checks if the password token is valid
        """
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPasswordView(generics.GenericAPIView):
    def patch(self, request):
        """
        Replaces the old password
        """
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class CheckRegisteredEmailView(generics.GenericAPIView):
    def post(self, request):
        """
        Checks if the email was already registered in the database
        """
        email = request.data.get('email')
        if email is None:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        is_registered = CustomUser.objects.filter(email=email).exists()
        return Response({'is_registered': is_registered})