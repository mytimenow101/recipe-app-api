from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)



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


    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

    def test_tag_str(self):
        """test the tags string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)


    def test_ingredient_str(self):
        """Test ingredient strin"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)