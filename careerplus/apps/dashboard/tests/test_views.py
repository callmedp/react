# django imports
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

# internal imports
from geolocation.models import Country


class TestRecommendedProduct(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user_data = {
            'email': 'testroot@gmail.com',
            'password': 'rootroot'}
        self.email = 'testroot@gmail.com'
        Country.objects.get_or_create(phone='91', name='India')
        self.inbox_url = reverse('dashboard:dashboard')
        self.myorder_url = reverse('dashboard:dashboard-myorder')
        self.wallet_url = reverse('dashboard:dashboard-mywallet')
        self.cookies = {}

    def setUpLogin(self):
        resp = self.client.post(
            '/login/', self.user_data, follow=True
        )
        # resp_status = ShineCandidateDetail().get_status_detail(
        #     email=self.email, shine_id=None, token=None)
        # if resp_status:
        #     resp.client.session.update(
        #         resp_status)
        #     resp.client.session.save()
        self.assertEqual(resp.status_code, 200)
        return resp

    def test_myinbox_without_login(self):
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, 302)

    def test_myorder_without_login(self):
        res = self.client.get(self.myorder_url)
        self.assertEqual(res.status_code, 302)

    def test_mywallet_without_login(self):
        res = self.client.get(self.wallet_url)
        self.assertEqual(res.status_code, 302)

    def test_myinbox_with_login(self):
        self.setUpLogin()
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, 200)

    def test_myorder_with_login(self):
        self.setUpLogin()
        res = self.client.get(self.myorder_url)
        self.assertEqual(res.status_code, 200)

    def test_mywallet_with_login(self):
        self.setUpLogin()
        res = self.client.get(self.wallet_url)
        self.assertEqual(res.status_code, 200)