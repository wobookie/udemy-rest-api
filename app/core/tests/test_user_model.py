import django.test
from core.models import User

def sample_user(username='testuser', password='Mypw-0123-ab#!', email='hello@mydomain.com'):
    # create a sample user
    return User.objects.create_user(username=username, email=email, password=password)

class UserModelTestCase(django.test.TestCase):

    def test_create_user_successful(self):
        # Test creating a new users with email is successful
        username='testuser'
        password='Mypw-0123-ab#!'
        email='hello@mydomain.com'

        user = sample_user(username=username, password=password, email=email)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # Test normalizing email is successful
        username = 'testuser'
        password = 'Mypw-0123-ab#!'
        email = 'hello@MyDomain.Com'

        user = sample_user(username=username, password=password, email=email)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_username(self):
        # Test creating users with no username raises error
        password = 'testpwd123'
        email = 'hello@MyDomain.Com'
        with self.assertRaises(ValueError):
            User.objects.create_user(username=None, password=password, email=email)

    def test_create_new_superuser(self):
        # Test creating a new superuser
        username = 'test.superuser'
        password = 'Mypw-0123-ab#!'
        user = User.objects.create_superuser(username=username, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_account_nopassword(self):
        # Test creating a new users with email is successful
        username = 'testuser'
        email = 'hello@mydomain.com'

        user = User.objects.create_user(username=username, password=None, email=email)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)