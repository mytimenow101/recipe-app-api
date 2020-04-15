from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """Function for creating user"""
    return get_user_model().objects.create_user(**params)

def setUp(self):
    """Instantiates neccessary variables for use later in the class"""
    self.client = APIClient()

def test_create_valid_user_success(self):
    """Test creating user with valid payload is successful"""
    payload = {
        'email': 'test@londonapp',
        'password': 'testpass',
        'name':'Test name'
    }
    res = self.client.post(CREATE_USER_URL,payload)

    self.asserEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    self.assertNotIn('password', res.data)

def test_user_user_exists(self):
    """Test if the user exists in the model fails"""
    payload = {'email':'email@mail.com', 'password': 'password1', 'name': 'test'}
    create_user(**payload)

    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

def test_create_token_for_user(self):
    """Test that a valid token was created for this user"""
    payload = {'email':'email@email.com', 'password':'password'}

    res = self.client.post(TOKEN_URL, payload)
    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

def test_create_token_invalid_credentials(self):
    """Test that a token is not created when the credential invalid"""
    payload = {'email':'email@email.com', 'password':'password'}
    create_user(**payload)
    payload = {'email':'email@email.com', 'password':'wrong'}

    res = self.client.post(TOKEN_URL,payload)

    self.asertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

def test_create_token_no_user(self):
    """Test token is not created if user not exists"""
    payload = {'email':'email@email.com', 'password':'password'}
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
