# django imports
from django.test import TestCase, Client
from shared.tests.factory.shared_factories import (
    ProductFactory, ProductWith4SkillsFactory
)

# internal imports
from geolocation.models import Country

class RecommendedApiView(TestCase):
    def setUp(self):
        self.client = Client()
        # user skills
        self.skills = 'Python,Django,Html,Css'
        Country.objects.get_or_create(
            phone='91', name='India')
        self.product = ProductWith4SkillsFactory(
            type_flow=2, type_product=0)

    def test_recommended_product_by_category_api(self):
        url = '/api/v1/recommended-products-by-category/?skills=' \
        + self.skills
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_recommended_product_api(self):
        url = '/api/v1/recommended-products/?skills=' + self.skills
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.json().get('results', [])))

    def test_recommended_product_api_with_blank_skills(self):
        url = '/api/v1/recommended-products/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(len(res.json().get('results', [])))
