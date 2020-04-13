from django.test import TestCase, Client
from django.urls import reverse
from core.models import User


class AdminSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='admin@domain.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email='test.user@domain.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        # Test that users are listed on user page
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        # Test that the user edit page works
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        # Test that the user create page works
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
