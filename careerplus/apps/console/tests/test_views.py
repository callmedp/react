# inbuilt  imports
import time

# third party imports
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Group

from geolocation.models import Country
from shop.models import Skill

from django.contrib.auth.models import Permission
from django.utils import timezone
from shared.tests.factory.shared_factories import (
    ProductFactory, OrderItemFactory, UserFactory,
    GroupFactory, CountryFactory, ProductAuditHistoryFactory,
    SkillFactory, FacultyFactory)
from core.mixins import TokenGeneration


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


class TestProductAuditHistoryView(TestCase):

    def setUp(self):
        self.user = None
        self.url = reverse('console:product-audit-history')
        CountryFactory()
        self.product = ProductFactory(type_flow=7)
        self.group = GroupFactory(name='FINANCE')
        self.user = UserFactory()
        ProductAuditHistoryFactory(
            product_id=self.product.id,
            product_name=self.product.name,
            variation_name=['N.A'],
            upc=self.product.upc,
            price=self.product.inr_price,
            duration=self.product.get_duration_in_day(),
            vendor_name=self.product.get_vendor()
        )

    def setUpLogin(self):
        self.client.post(
            '/console/login/', {'username': 'ritesh.bisht93@gmail.com', 'password': '12345'}
        )

    def setUpGroup(self):
        self.group.user_set.add(self.user)

    def setupUserAndGroup(self):
        self.setUpGroup()
        self.setUpLogin()

    def removeFromGroup(self):
        self.group.user_set.remove(self.user)

    def test_not_allowed_for_non_logged_in_user(self):
        self.client = Client()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_allowed_for_logged_in_user_with_permisssion(self):
        self.setupUserAndGroup()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_not_allowed_for_logged_in_without_permission(self):
        self.removeFromGroup()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_correct_template_loaded(self):
        self.setupUserAndGroup()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'console/tasks/product-audit-history.html')

    def test_data_is_bieng_loaded_with_correct_product_id_and_date_range(self):
        self.setupUserAndGroup()
        data = {
            'product_id': self.product.id,
            'date_range': '07/11/2018 - 09/11/2018'
        }
        response = self.client.get(self.url, data)
        self.assertTrue(len(response.context['page'].object_list))

    def test_data_is_not_loaded_with_incorrect_product_id_and_date_range(self):
        self.setupUserAndGroup()
        data = {
            'product_id': self.product.id,
            'date_range': '07/11/2018 - 07/13/2018'
        }
        response = self.client.get(self.url, data)
        self.assertFalse(len(response.context['page'].object_list))


class TestProductHistoryLogDownloadView(TestCase):

    def setUp(self):
        self.user = None
        self.url = reverse('console:product-audit-history-download')
        CountryFactory()
        self.product = ProductFactory(type_flow=7)
        self.group = GroupFactory(name='FINANCE')
        self.user = UserFactory()
        ProductAuditHistoryFactory(
            product_id=self.product.id,
            product_name=self.product.name,
            variation_name=['N.A'],
            upc=self.product.upc,
            price=self.product.inr_price,
            duration=self.product.get_duration_in_day(),
            vendor_name=self.product.get_vendor()
        )

    def setUpLogin(self):
        self.client.post(
            '/console/login/', {'username': 'ritesh.bisht93@gmail.com', 'password': '12345'}
        )

    def setUpGroup(self):
        self.group.user_set.add(self.user)

    def setupUserAndGroup(self):
        self.setUpGroup()
        self.setUpLogin()

    def removeFromGroup(self):
        self.group.user_set.remove(self.user)

    def test_not_allowed_for_non_logged_in_user(self):
        self.client = Client()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_not_allowed_for_logged_in_user_with_permisssion(self):
        self.setupUserAndGroup()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_not_allowed_for_logged_in_without_permission(self):
        self.removeFromGroup()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_csv_file_returned_with_product_id_and_date_range_is_empty(self):
        self.setupUserAndGroup()
        data = {
            'product_id': self.product.id,
            'date_range': '05/11/2018 - 06/11/2018'
        }
        response = self.client.post(self.url, data, follow=True)
        file_name = 'no_log' + timezone.now().date().strftime("%Y-%m-%d")
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=" + file_name + ".csv"
        )

    def test_csv_file_returned_with_product_id_and_date_range_is_not_empty(self):
        self.setupUserAndGroup()
        data = {
            'product_id': self.product.id,
            'date_range': '07/11/2018 - 09/11/2018'
        }
        response = self.client.post(self.url, data, follow=True)
        file_name = self.product.name + timezone.now().date().strftime("%Y-%m-%d")
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=" + file_name + ".csv"
        )

    def test_error_occured_with_no_product_id(self):
        self.setupUserAndGroup()
        data = {
            'date_range': '07/11/2018 - 09/11/2018'
        }
        response = self.client.post(self.url, data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please select Product and Date Range')


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


class TestConsoleAutoLoginView(TestCase):

    url = reverse('console:autologin')
    user = UserFactory()

    def setUp(self):
        self.user = UserFactory()
        self.data = {
            'token': TokenGeneration().encode(self.user.email, 2, 1)
        }

    def test_invalid_token_message_for_incorrect_token(self):
        self.data['token'] = 'Invalid token'
        response = self.client.get(self.url, self.data, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Token has been expired. Login with Username/Password ', str(message))

    def test_login_with_valid_token(self):
        response = self.client.get(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].email, self.user.email)


class TestFacultyConsoleView(TestCase):
    def setUp(self):
        self.client = Client()
        Country.objects.get_or_create(
            phone='91', name='India')
        self.faculty = FacultyFactory(name="Faculty")
        self.add_url = reverse('console:faculty-add')
        self.list_url = reverse('console:faculty-list')
        self.change_url = reverse(
            'console:faculty-change',
            kwargs={'pk': self.faculty.pk})
        self.user = UserFactory(
            name="root", email='testroot@gmail.com',
            password="rootroot")
        self.add_perm = Permission.objects.get(
            name='Can Add Faculty From Console')
        self.change_perm = Permission.objects.get(
            name='Can Change Faculty From Console')
        self.view_perm = Permission.objects.get(
            name='Can View Faculty From Console')

    def setUpLogin(self):
        time.sleep(2)
        self.client.post(
            '/console/login/', {
                'username': 'testroot@gmail.com',
                'password': 'rootroot'}
        )

    def setUpPermission(self):
        self.user.user_permissions.add(self.add_perm)
        self.user.user_permissions.add(self.change_perm)
        self.user.user_permissions.add(self.view_perm)

    def removePermission(self):
        self.user.user_permissions.remove(self.add_perm)
        self.user.user_permissions.remove(self.change_perm)
        self.user.user_permissions.remove(self.view_perm)

    def test_add_faculty_with_permission(self):
        self.setUpLogin()
        self.setUpPermission()
        res = self.client.get(self.add_url)
        self.assertEqual(res.status_code, 200)

    def test_add_faculty_without_permission(self):
        self.setUpLogin()
        self.removePermission()
        res = self.client.get(self.add_url)
        self.assertEqual(res.status_code, 403)

    def test_list_faculty_with_permission(self):
        self.setUpLogin()
        self.setUpPermission()
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

    def test_list_faculty_without_permission(self):
        self.setUpLogin()
        self.removePermission()
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 403)

    def test_change_faculty_with_permission(self):
        self.setUpLogin()
        self.setUpPermission()
        res = self.client.get(self.change_url)
        self.assertEqual(res.status_code, 200)

    def test_change_faculty_without_permission(self):
        self.setUpLogin()
        self.removePermission()
        res = self.client.get(self.change_url)
        self.assertEqual(res.status_code, 403)