from django.urls import path
from login.views import LoginView, RegisterView,CheckRegisteredEmailView, VerifyEmailView, SetNewPasswordView, RequestPasswordResetView, PasswordTokenCheckView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('request-reset-email/', RequestPasswordResetView.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordView.as_view(), name='password-reset-complete'),
    path('check-registered-email/', CheckRegisteredEmailView.as_view(), name='check-registered-email'),
]
