from django.test import TestCase, Client
from django.urls import reverse
from geolocation.models import Country
from django.contrib.auth.models import Permission
from django.utils import timezone
from shared.tests.factory.shared_factories import \
    ProductFactory, OrderItemFactory, UserFactory, \
    GroupFactory, CountryFactory, ProductAuditHistoryFactory


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

    def test_do_not_load_product_with_incorrect_ops_status(self):
        self.setupUserAndPermission()
        orderitem = self.orderitem
        orderitem.oi_status = 61
        orderitem.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_do_not_load_product_with_incorrect_product_type_flow(self):
        self.setupUserAndPermission()
        product = self.orderitem.product
        product.type_flow = 8
        product.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

    def test_do_not_load_product_with_incorrect_wc_sub_category(self):
        self.setupUserAndPermission()
        incorrect_wc_cub_category = [64, 65]
        for status in incorrect_wc_cub_category:
            orderitem = self.orderitem
            orderitem. wc_sub_cat = status
            orderitem.save()
            response = self.client.get(self.url)
            self.assertFalse(len(response.context['page'].object_list))

    def test_do_not_load_product_with_no_process_true(self):
        self.setupUserAndPermission()
        orderitem = self.orderitem
        orderitem.no_process = True
        orderitem.save()
        response = self.client.get(self.url)
        self.assertFalse(len(response.context['page'].object_list))

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
