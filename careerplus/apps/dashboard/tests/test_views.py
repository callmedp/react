
# django imports
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

# internal imports
from geolocation.models import Country
from core.api_mixin import ShineCandidateDetail


class TestRecommendedProduct(TestCase):
    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.user_data = {'email': 'testroot@gamil.com', 'password': 'rootroot'}
        self.email = 'testroot@gmail.com'
        Country.objects.get_or_create(phone='91', name='India')
        self.inbox_url = reverse('dashboard:dashboard')
        self.myorder_url = reverse('dashboard:dashboard-myorder')
        self.wallet_url = reverse('dashboard:dashboard-mywallet')

    def setUpLogin(self):
        import ipdb; ipdb.set_trace()
        resp = self.client.post(
            '/login/', self.user_data
        )
        resp_status = ShineCandidateDetail().get_status_detail(
            email=self.email, shine_id=None, token=None)
        if resp_status:
            resp.client.session.update(
                resp_status)
            resp.client.session.save()
        self.assertEqual(resp.status_code, 200)
        return resp.context['request']

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
        request = self.setUpLogin()
        import ipdb; ipdb.set_trace()
        res = self.client.get(self.inbox_url)