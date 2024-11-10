from django.test import TestCase, Client

from content.utils import create_custom_user
from login.models import CustomUser

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

