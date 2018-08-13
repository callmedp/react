from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group

from geolocation.models import Country
from shop.models import Skill

from django.contrib.auth.models import Permission
from shared.tests.factory.shared_factories import \
    ProductFactory, OrderItemFactory, UserFactory,\
    SkillFactory


class TestBoosterQueueView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = None
        self.url = reverse('console:queue-booster')
        self.permission = Permission.objects.get(name='can show booster queue')
        Country.objects.get_or_create(phone='91', name='India')
        self.product = ProductFactory(type_flow=7)
        self.orderitem = OrderItemFactory(product=self.product, order__status=1, oi_status=5)
        self.user = UserFactory()

    def setupUserAndPermission(self):
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

    def test_redirect_for_non_logged_in_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_method_allowed_for_logged_in_user_with_permission(self):
        self.setupUserAndPermission()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redirect_logged_in_user_without_permission(self):
        self.removePermission()
        self.setUpLogin()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_correct_template_loaded(self):
        self.setupUserAndPermission()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'console/order/booster-list.html')

    def test_unpaid_product_is_not_loaded(self):
        self.setupUserAndPermission()
        order = self.orderitem.order
        order.status = 0
        order.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_paid_product_is_loaded(self):
        self.setupUserAndPermission()
        response = self.client.get(self.url)
        self.assertTrue(len(response.context['page'].object_list))

    def test_welcome_call_not_done_product_is_not_loaded(self):
        self.setupUserAndPermission()
        order = self.orderitem.order
        order.welcome_call_done = False
        order.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_welcome_call_done_product_loaded(self):
        self.setupUserAndPermission()
        response = self.client.get(self.url)
        self.assertTrue(len(response.context['page'].object_list))

    def test_load_product_with_correct_ops_status(self):
        self.setupUserAndPermission()
        correct_oi_status = [5, 62]
        for status in correct_oi_status:
            orderitem = self.orderitem
            orderitem.oi_status = status
            orderitem.save()
            response = self.client.get(self.url)
            self.assertTrue(len(response.context['page'].object_list))

    def test_load_product_with_incorrect_ops_status(self):
        self.setupUserAndPermission()
        orderitem = self.orderitem
        orderitem.oi_status = 61
        orderitem.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_load_product_with_incorrect_product_type_flow(self):
        self.setupUserAndPermission()
        product = self.orderitem.product
        product.type_flow = 8
        product.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_load_product_with_incorrect_wc_sub_category(self):
        self.setupUserAndPermission()
        incorrect_wc_cub_category = [64, 65]
        for status in incorrect_wc_cub_category:
            orderitem = self.orderitem
            orderitem. wc_sub_cat = status
            orderitem.save()
            response = self.client.get(self.url)
            self.assertFalse(len(response.context['page'].object_list))

    def test_load_product_with_no_process_true(self):
        self.setupUserAndPermission()
        orderitem = self.orderitem
        orderitem.no_process = True
        orderitem.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_upload_draft_for_resume_booster_product(self):
        self.setupUserAndPermission()
        with open(settings.BASE_DIR + '/apps/shared/tests/files/resume.docx') as upload_draft:
            response = self.client.post(
                self.url,
                {'oi_pk': self.orderitem.pk, 'oi_resume': upload_draft},
                follow=True
            )
        message = list(response.context['messages'])[0]
        self.assertEqual('Draft uploaded Successfully', str(message))

    def test_upload_draft_with_wrong_extension(self):
        self.setupUserAndPermission()
        with open(settings.BASE_DIR + '/apps/shared/tests/files/resume.xls') as upload_draft:
            response = self.client.post(
                self.url,
                {'oi_pk': self.orderitem.pk, 'oi_resume': upload_draft},
                follow=True
            )
        message = list(response.context['messages'])[0]
        self.assertEqual('only pdf, doc and docx formats are allowed.', str(message))

    def test_upload_empty_draft(self):
        self.setupUserAndPermission()
        with open(settings.BASE_DIR + '/apps/shared/tests/files/empty_resume.docx') as upload_draft:
            response = self.client.post(
                self.url,
                {'oi_pk': self.orderitem.pk, 'oi_resume': upload_draft},
                follow=True
            )
        message = list(response.context['messages'])[0]
        self.assertEqual('The submitted file is empty.', str(message))

    def test_upload_draft_wihtout_file(self):
        self.setupUserAndPermission()
        response = self.client.post(
            self.url,
            {'oi_pk': self.orderitem.pk},
            follow=True
        )
        message = list(response.context['messages'])[0]
        self.assertEqual('This field is required.', str(message))

    def test_upload_draft_with_greater_size(self):
        self.setupUserAndPermission()
        with open(settings.BASE_DIR + '/apps/shared/tests/files/resume_max_size.docx') as upload_draft:
            response = self.client.post(
                self.url,
                {'oi_pk': self.orderitem.pk, 'oi_resume': upload_draft},
                follow=True
            )
        message = list(response.context['messages'])[0]
        self.assertEqual('resume is too large ( > 500kb ).', str(message))

    def test_upload_draft_for_with_wrong_orderitem(self):
        self.setupUserAndPermission()
        with open(settings.BASE_DIR + '/apps/shared/tests/files/resume.docx') as upload_draft:
            response = self.client.post(
                self.url,
                {'oi_pk': self.orderitem.pk + 21, 'oi_resume': upload_draft},
                follow=True
            )
        message = list(response.context['messages'])[0]
        self.assertEqual('OrderItem matching query does not exist.', str(message))

    def tearDown(self):
        self.orderitem.order.delete()
        self.product.delete()


class TestSkillAddAndListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = None
        self.url = reverse('console:skill-add')
        Country.objects.get_or_create(phone='91', name='India')
        self.user = UserFactory(
            name="root", email='testroot@gmail.com',
            password="rootroot")
        self.skill = SkillFactory(name='Skill', active=True)

    def setUpLogin(self):
        resp = self.client.post(
            '/console/login/',
            {
                'username': 'testroot@gmail.com',
                'password': 'rootroot'}
        )
        return resp

    def setPermission(self):
        group, created = Group.objects.get_or_create(
            name=settings.PRODUCT_GROUP_LIST[0]
        )
        group.user_set.add(self.user)

    def removePermission(self):
        group, created = Group.objects.get_or_create(
            name=settings.PRODUCT_GROUP_LIST[0]
        )
        group.user_set.remove(self.user)

    def delete_skill(self, name='Java'):
        skill = Skill.objects.filter(name=name)
        if skill.exists():
            skill.delete()

    def test_skill_add_without_login(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post(self.url, {'name': 'Skill'})
        self.assertEqual(resp.status_code, 302)

    def test_skill_add_without_permission(self):
        resp = self.setUpLogin()
        self.removePermission()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_skill_add_with_permission(self):
        self.setUpLogin()
        self.setPermission()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

        self.delete_skill(name='Java')
        resp = self.client.post(
            self.url, {'name': 'Java', }, follow=True)
        message = list(resp.context['messages'])[0]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            'You have successfully added a Skill',
            str(message))

    def test_skill_list_view(self):
        self.setUpLogin()
        self.setPermission()
        url = reverse('console:skill-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['skill_list']))