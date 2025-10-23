from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Community, CommunityLeader


class DashboardTests(TestCase):
    def setUp(self):
        self.community = Community.objects.create(name='Dash C', description='d', location='City')
        self.user = User.objects.create_user(username='leader', password='pass12345')
        self.group, _ = Group.objects.get_or_create(name='leader')
        self.user.groups.add(self.group)
        CommunityLeader.objects.create(user=self.user, community=self.community)

    def test_dashboard_requires_login(self):
        resp = self.client.get('/dashboard/leader/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp['Location'])

    def test_dashboard_renders_for_leader(self):
        self.client.login(username='leader', password='pass12345')
        resp = self.client.get('/dashboard/leader/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Leader Dashboard')
        self.assertContains(resp, 'Dash C')
        # shows 'Your communities' section and manage link
        self.assertContains(resp, 'Your communities')

    def test_new_community_upgrades_to_leader(self):
        # Participant user
        user = User.objects.create_user(username='participant', password='pass12345')
        self.client.login(username='participant', password='pass12345')
        data = {
            'name': 'My Community',
            'tagline': 'Tag',
            'description': 'Short desc',
            'about': 'About',
            'location': 'City',
            'contact_email': 'test@example.com',
            'website_url': 'https://example.com',
            'logo_url': '',
        }
        resp = self.client.post('/communities/new/', data)
        self.assertEqual(resp.status_code, 302)
        # Redirect to dashboard and leader link exists
        self.assertTrue(CommunityLeader.objects.filter(user=user).exists())
        # After redirect, dashboard should show the new community in "Your communities"
        resp2 = self.client.get('/dashboard/leader/')
        self.assertContains(resp2, 'My Community')
