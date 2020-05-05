from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """Test public api"""

    def setUp(self):
        self.client = APIClient()


    def test_login_required(self):
        """Test login"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    class PrivateIngredientsApiTest(TestCase):
        """Test authorized is needed"""
        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create(
                'test@london@mail.com',
                'tespass'
            )
            self.client.force_authentication(self.user)
        
        def test_retrieve_ingredients_list(self):
            """Test if we can get list of ingredients"""    
            Ingredients.objects.create(user=self.user, name='Kale')
            Ingredients.objects.create(user=self.user, name='Sugar')

            res = self.client.get(INGREDIENTS_URL)

            ingredients = Ingredients.objects.all().order_by('-name')
            serializer = IngredientSerializer(ingredients, many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, serializer.data)

        def test_ingredients_limited_to_user(self):
            """That ingredients for the authenticated users are returned"""
            user2 = get_user_model().objects.create(
                'mail@email.com',
                'password'
            )
            
            Ingredients.objects.create(user=self.user2, name='pepper')
            ingredient = Ingredients.objects.create(user=self.user,name='buns')

            res = self.client.get(INGREDIENTS_URL)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(len(res.data), 1)
            self.assertEqual(res.datat[0]['name'],ingredient.name )

        def test_create_ingredient_successful(self):
            """Test that we can add ingredient"""
            payload = {'name': 'Cabbage'}
            self.client.post(INGREDIENT_URL, payload)

            exist = Ingredient.objecst.filter(user=self.user,name=payload).exists

            self.assertTrue(exist)
        
        def test_create_ingredient_invalid(self):
            """Try to make invalid ingredient"""
            payload = {'name':''}

            res = self.client.post(INGREDIENT_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)













