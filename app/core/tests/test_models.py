from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test that creating a user with new email is working"""
        email = 'mytimenow@gmail.com'
        password = 'password'

        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

def test_new_user_email_normalized(self):
    """Test that the email is normalized"""
    email = 'test@LONDONAPPDEV.COM'
    user = get_user_model().objects.create_user(email, 'test1213')

    self.assertEqual(user.email, email.lower())


def test_create_new_superuser():
    """Test creating new superuser"""
    user = get_user_model().objects.create_superuser(
        'test@gmail.com',
        'test123'
    )
