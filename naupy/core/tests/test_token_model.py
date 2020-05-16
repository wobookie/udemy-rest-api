import django.test
import os
import binascii
# from core.models import APIToken

def generate_token(len=20):
    return binascii.hexlify(os.urandom(len)).decode()

class APITokenModelTestCase(django.test.TestCase):

    def test_create_token_successful(self):
        # Test creating a new token
        token = generate_token()

        self.assertEqual(token, token)