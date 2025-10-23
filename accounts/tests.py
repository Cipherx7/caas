from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthFlowTests(TestCase):
    def test_login_page_loads(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Demo credentials')

    def test_signup_creates_user_and_redirects(self):
        data = {
            'username': 'newuser',
            'password1': 'StrongPass12345',
            'password2': 'StrongPass12345',
        }
        resp = self.client.post(reverse('signup'), data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
