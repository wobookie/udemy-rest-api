from django.test import TestCase
from django.urls import reverse

from core.models import User

import logging
logger = logging.getLogger('unit-test')

LOGIN_USER_URL = reverse('web:login')
HOME_URL = reverse('web:home')
TOKENS_URL = reverse('web:tokens')


class WebTestCase(TestCase):
    # Test the web login page
    def setUp(self):
        self.username_1 = 'test.user.1'
        self.password_1 = 'XIab-1754-?#<>'
        User.objects.create_user(username=self.username_1, password=self.password_1)

        self.username_2 = 'test.user.2'
        self.password_2 = None
        User.objects.create_user(username=self.username_2, password=self.password_2)

    def test_redirect_from_home_if_not_logged_in(self):
        response = self.client.get(HOME_URL)
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/web/login'))

    def test_redirect_from_login_if_invalid_credentials(self):
        self.client.login(username=self.username_1, password='invalid')
        response = self.client.get(HOME_URL)
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/web/login'))

    def test_redirect_from_login_if_no_password(self):
        self.client.login(username=self.username_2, password=self.password_2)
        response = self.client.get(HOME_URL)
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/web/login'))

    def test_uses_correct_template(self):
        self.client.login(username=self.username_1, password=self.password_1)
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'web/home.html')
