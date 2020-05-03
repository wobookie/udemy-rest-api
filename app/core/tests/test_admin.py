from django.test import TestCase, Client
from django.urls import reverse
from core.models import User


class AdminSiteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='password123'
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email='test.users@domain.com',
            password='password123',
            username='test.name'
        )

    def test_users_listed(self):
        # Test that users are listed on users page
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        # Test that the users edit page works
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        # Test that the users create page works
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
