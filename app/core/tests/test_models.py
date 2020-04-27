import django.test
from core.models import User


class MyTestCase(django.test.TestCase):
    def test_create_user_with_email_successful(self):
        # Test creating a new users with email is successful
        email = 'test.users@mydomain.com'
        password = 'testpwd123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # Test normalizing email is successful
        email = 'test.users@MYDOMAIN.COM'
        password = 'testpwd123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # Test creating users with no email raises error
        password = 'testpwd123'
        with self.assertRaises(ValueError):
            User.objects.create_user(None, password=password)

    def test_create_new_superuser(self):
        # Test creating a new superuser
        email = 'test.superuser@mydomain.com'
        password = 'testpwd123'
        user = User.objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
