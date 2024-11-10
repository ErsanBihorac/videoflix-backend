from django.test import TestCase, Client
from django.urls import reverse
from content.utils import create_custom_user
from login.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
import jwt
from django.conf import settings
class TestModels(TestCase):
    def setUp(self):
        self.user = create_custom_user()

    def test_model_custom_user(self):
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(self.user.email, 'test@mail.com')
        self.assertTrue(self.user.check_password('testing_password'))
        self.assertEqual(self.user.is_verified, False)
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        create_custom_user()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register_post(self):
        response = self.client.post(self.register_url, data={'email': 'new_test@mail.com', 'password': 'new_testing_password'})
        self.assertEqual(response.status_code, 201)

    def test_login_post_unauthenticated(self):
        response = self.client.post(self.login_url, data={'email': 'test@mail.com', 'password': 'testing_password'})
        self.assertEqual(response.status_code, 401)

class VerifyEmailViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.verify_email_url = reverse('email-verify')

        self.user_data = {
            'email': 'test@mail.com',
            'password': 'testing_password',
        }

        self.user = get_user_model().objects.create_user(**self.user_data)
        self.token = RefreshToken.for_user(self.user).access_token
        self.confirmation_link = f"http://testserver{self.verify_email_url}?token={str(self.token)}"

    def test_email_verification_success(self):
        response = self.client.get(self.confirmation_link)
        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(email=self.user_data['email'])
        self.assertTrue(user.is_verified)

    def test_invalid_token(self):
        invalid_token = 'invalidtokenstring'
        response = self.client.get(f"{self.verify_email_url}?token={invalid_token}")
        self.assertEqual(response.status_code, 400)

    def test_expired_token(self):
        expired_token = jwt.encode({'user_id': self.user.id, 'exp': 0}, settings.SECRET_KEY, algorithm='HS256')
        response = self.client.get(f"{self.verify_email_url}?token={expired_token}")
        self.assertEqual(response.status_code, 400)