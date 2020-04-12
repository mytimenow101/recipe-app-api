from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Used for testing the admin pages"""
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'starboy@gmail.com',
            password = 'password'
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email = 'test@tes.com',
            password = 'password',
            name ='Test user'
        )

    def test_urls_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works in admin"""
        url =  revers('admin:core_user_change')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)