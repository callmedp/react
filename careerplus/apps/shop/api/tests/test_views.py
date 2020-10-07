import json

from django.test import TestCase
from shared.tests.factory.shared_factories import \
    UserFactory, ProductFactory, CountryFactory


class TestProductListView(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.country = CountryFactory()
        self.url = '/api/v1/products/'

    def setUpLogin(self):
        self.client.post(
            '/console/login/', {'username': 'ritesh.bisht93@gmail.com', 'password': '12345'}
        )

    def test_allowed_for_logged_in_user(self):
        self.setUpLogin()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_for_non_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_empty_results_without_vendor_id(self):
        self.setUpLogin()
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 0)

    def test_return_correct_result_with_vendor_id(self):
        self.setUpLogin()
        response = self.client.get(self.url + '?vendor=' + str(self.product.vendor.id)+'&fl=id,name')
        self.assertEqual(response.data['count'], 1)
        results = response.data['results'][0]
        result_keys = json.loads(json.dumps(results)).keys()
        expected_keys = ['id', 'name']
        for key in result_keys:
            self.assertIn(key, expected_keys)
