
# django imports
from django.test import TestCase, Client

# internal imports
from geolocation.models import Country
from search.helpers import get_recommendations


class TestRecommendedProduct(TestCase):
    def setUp(self):
        self.client = Client()
        self.func_area = None
        # user skills
        self.skills = ['244', '310', '4', '10', '320', '389', '3827', '3824']
        self.user_data = {'email': 'testroot@gamil.com', 'password': 'rootroot'}
        self.email = 'testroot@gmail.com'
        Country.objects.get_or_create(phone='91', name='India')

    def setUpLogin(self):
        resp = self.client.post(
            '/login/', self.user_data
        )
        resp.context['request'].session.update({
            'email': self.email,
            'skills': self.skills})
        self.assertEqual(resp.status_code, 200)
        return resp

    def test_product_recommended_with_login(self):
        resp = self.setUpLogin()
        request = resp.context['request']
        skills = request.session.get(
            'skills', self.skills)
        self.assertTrue(len(skills))
        rec_prds = get_recommendations(self.func_area, skills)
        self.assertTrue(len(rec_prds))

    def test_product_recommended_anonymous_user(self):
        skills = self.client.session.get(
            'skills', [])
        self.assertFalse(len(skills))
        rec_prds = get_recommendations(self.func_area, skills)
        self.assertFalse(len(rec_prds))
