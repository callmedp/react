import datetime

from django.test import TestCase

from shared.tests.factory.shared_factories import (
    AdminFactory, UserFactory, WriterFactory,
    OrderItemFactory, ProductFactory)
from users.mixins import WriterInvoiceMixin


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


class TestWriterInvoice(TestCase):
    def setUp(self):
        self.writer = WriterFactory()
        self.product = ProductFactory()
        self.product.active = True
        self.product.type_flow = 1
        self.product.type_product = 0
        self.product.save()
        self.today_date = datetime.datetime.now()
        first_day = self.today_date.replace(day=1)
        prev_month = first_day - datetime.timedelta(days=1)
        last_month_first_day = prev_month.replace(day=1)
        assigned_date = last_month_first_day + datetime.timedelta(
            days=5)
        closed_on = assigned_date + datetime.timedelta(days=5)
        self.oi = OrderItemFactory()
        self.oi.assigned_date = assigned_date
        self.oi.closed_on = closed_on
        self.oi.assigned_to = self.writer
        self.oi.oi_status = 4
        self.oi.order.status = 1
        self.oi.product = self.product
        self.oi.save()
        self.oi.order.save()

    def test_writer_obj(self):
        self.writer.userprofile.writer_type = 1
        self.writer.userprofile.pan_no = "pan_no"
        self.writer.userprofile.gstin = "gstin"
        self.writer.userprofile.address = "Gurgaon"
        self.writer.userprofile.po_number = "98765"
        self.writer.userprofile.valid_from = datetime.datetime.today(
            ) - datetime.timedelta(
            days=100)
        self.writer.userprofile.valid_to = datetime.datetime.today(
            ) + datetime.timedelta(
            days=100)
        self.writer.userprofile.save()
        return self.writer
    def test_writer_invoice_with_standalone_oi(self):
        self.oi.no_process = False
        self.oi.is_combo = False
        self.oi.is_variation = False
        self.oi.is_addon = False
        self.oi.save()

        res = WriterInvoiceMixin().save_writer_invoice_pdf(
            user=self.writer)

        self.assertEqual(res.get('error', None), '')
        self.assertTrue(len(res.get('item_list', [])))

    def test_writer_invoice_with_addon_oi(self):
        self.oi.no_process = False
        self.oi.is_combo = False
        self.oi.is_variation = False
        self.oi.is_addon = True
        self.oi.save()

        res = WriterInvoiceMixin().save_writer_invoice_pdf(
            user=self.writer)

        self.assertEqual(res.get('error', None), '')
        self.assertTrue(len(res.get('item_list', [])))


    def tearDown(self):
        # Clean up run after every test method.
        pass
