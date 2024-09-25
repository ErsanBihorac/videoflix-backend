from django.urls import path
from login.views import LoginView, RegisterView, VerifyEmailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
]
