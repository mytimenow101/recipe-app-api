from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Used for testing the admin pages"""
    def setup(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'starboy@gmail.com',
            password = 'password'
        )

        self.client.force_login(self.admim_user)

        self.user = get_user_model().objects.create_user(
            email = 'test@tes.com',
            password = 'password',
            name ='Test user'
        )

     def test_urls_listed(self):
         """the uses are listed on a page"""
         url = reverse('admin:core_user_changelist')

         self.assertContains(res, self.user.name)
         self.assertContains(res, self.user.email)
