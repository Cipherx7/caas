from django.test import TestCase
from django.urls import reverse
from .models import Community, Sponsor, Sponsorship

class DirectoryViewTests(TestCase):
    def setUp(self):
        Community.objects.create(name="Test A", description="desc", location="Mumbai", verified=True)
        Community.objects.create(name="Test B", description="desc", location="Pune", verified=False)

    def test_directory_renders(self):
        resp = self.client.get(reverse('communities_directory'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test A")
        self.assertContains(resp, "Test B")

    def test_filter_verified(self):
        resp = self.client.get(reverse('communities_directory') + "?verified=on")
        self.assertContains(resp, "Test A")
        self.assertNotContains(resp, "Test B")

    def test_detail_view(self):
        c = Community.objects.create(name="Detail C", description="desc", location="Goa", verified=True)
        s = Sponsor.objects.create(name="Acme")
        Sponsorship.objects.create(community=c, sponsor=s, amount=1000, contribution_type='cash', date='2025-01-01')
        resp = self.client.get(reverse('community_detail', args=[c.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Detail C")
        self.assertContains(resp, "₹1,000")
