from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import logging

CREATE_USER_URL = reverse('users:create')
OBTAIN_TOKEN_URL = reverse('users:token_obtain')
REFRESH_TOKEN_URL = reverse('users:token_refresh')

LOGGER = logging.getLogger('unittest')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    # Test the users API (public)

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # Test creating a users with valid payload
        payload = {
            'email': 'test@test.com',
            'password': 'mysecretpassword',
            'username': 'test.name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        # Test creating users that exists fails
        payload = {
            'email': 'test@test.com',
            'password': 'mysecretpassword',
            'username': 'test.name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # Test password meets length
        payload = {
            'email': 'test@test.com',
            'password': 'pw',
            'username': 'test.name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_password_similar(self):
        # Test password meets length
        payload = {
            'email': 'test@test.com',
            'password': 'test1.name',
            'username': 'test.name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # Test that a token is created for the users
        payload = {
            'username': 'test.name',
            'password': 'p@ssphras3'
        }
        create_user(**payload)
        res = self.client.post(OBTAIN_TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        # Test that a token is not created if invalid credentials are given
        create_user(username='test.name', password='p@ssphras3')
        payload = {
            'username': 'test.name',
            'password': 'passphrase'
        }
        res = self.client.post(OBTAIN_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_no_user(self):
        # Test that a token is not created if users does not exists
        payload = {
            'username': 'test.name',
            'password': 'p@ssphras3'
        }
        res = self.client.post(OBTAIN_TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertNotIn('refresh', res.data)
        self.assertEqual('No active account found with the given credentials', res.data['detail'])
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)