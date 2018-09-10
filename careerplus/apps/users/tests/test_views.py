from django.test import TestCase
from shared.tests.factory.shared_factories import AdminFactory, UserFactory


class TestUserLoginTokenView(TestCase):

    url = '/admin/autologintoken/'

    def setUp(self):
        self.admin = AdminFactory()
        self.user = UserFactory()

    def setUpLogin(self):
        self.client.post(
            '/admin/login/', {'username': 'root@root.com', 'password': '12345'}
        )

    def test_redirect_non_logged_in_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_correct_template_loaded(self):
        self.setUpLogin()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'admin/users/autologin.html')

    def test_email_does_not_exist_for_token(self):
        self.setUpLogin()
        response = self.client.post(self.url, {'email': 'ritesh.bisht1994@gmail.com'})
        message = list(response.context['messages'])[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Provided Email Does Not Exist', str(message))

    def test_login_url_exist_in_context(self):
        self.setUpLogin()
        response = self.client.post(self.url, {'email': 'ritesh.bisht93@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('login_url', response.context)
