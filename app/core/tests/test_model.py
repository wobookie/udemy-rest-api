import unittest
from django.contrib.auth.models import User


class MyTestCase(unittest.TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'test@heims-family.me'
        password = 'testpwd123'


        user = User(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test normalizing email is successful"""
        email = 'test@HEIMS-FAMILY.com'
        password = 'testpwd123'
        user = User(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())


if __name__ == '__main__':
    unittest.main()
