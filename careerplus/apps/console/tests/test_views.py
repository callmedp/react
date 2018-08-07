from django.test import TestCase, Client
from django.urls import reverse
from geolocation.models import Country
from django.contrib.auth.models import Permission
from users.models import User
from shared.tests.factory.shared_factories import ProductFactory


class TestBoosterQueueView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = None
        self.url = reverse('console:queue-booster')
        self.permission = Permission.objects.get(name='can show booster queue')
        Country.objects.get_or_create(phone='91', name='India')

    def setUpUser(self):
        self.user, created = User.objects.get_or_create(name='ritesh', email='ritesh.bisht93@gmail.com')
        self.user.set_password('12345')
        self.user.save()

    def setupUserAndPermission(self):
        self.setUpUser()
        self.setUpPermission()
        self.setUpLogin()

    def setUpPermission(self):
        self.user.user_permissions.add(self.permission)

    def removePermission(self):
        self.user.user_permissions.remove(self.permission)

    def setUpLogin(self):
        self.client.post(
            '/console/login/', {'username': 'ritesh.bisht93@gmail.com', 'password': '12345'}
        )

    def setUpBoosterProduct(self):
        self.resume_booster_product = ProductFactory(type_flow=7)
        self.resume_writing_product = ProductFactory(type_flow=1)

    def test_redirect_for_non_logged_in_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_method_allowed_for_logged_in_user_with_permission(self):
        self.setupUserAndPermission()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redirect_logged_in_user_without_permission(self):
        self.setUpUser()
        self.removePermission()
        self.setUpLogin()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_correct_template_loaded(self):
        self.setupUserAndPermission()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'console/order/booster-list.html')
