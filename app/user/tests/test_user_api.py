from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    # Test the users API (public)

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # Test creating a user with valid payload
        payload = {
            'email' : 'test@test.com',
            'password' : 'mysecretpassword',
            'name': 'test-name, last'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        # Test creating user that exists fails
        payload = {
            'email' : 'test@test.com',
            'password' : 'mysecretpassword',
            'name': 'test-name, last'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # Test password meets length
        payload = {
            'email' : 'test@test.com',
            'password' : 'pw',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_password_similar(self):
        # Test password meets length
        payload = {
            'email' : 'test@test.com',
            'password' : 'test_test_1',
            'name': 'test_test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)