from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .models import Page, Widget
from .views import CMSPageView

User = get_user_model()


class TestsPage(TestCase):
	# fixtures = ['test.json']

	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()
		self.user = User.objects.create_user(
			email='test@gmail.com', password='test@123')

	def test_get_template_method(self):
		widget = Widget(widget_type=1)
		self.assertEqual(widget.get_template(), 'text_format.html')
		widget = Widget(widget_type=2)
		self.assertEqual(widget.get_template(), 'download_pdf.html')
		widget = Widget(widget_type=3)
		self.assertEqual(widget.get_template(), 'related_blog.html')
		widget = Widget(widget_type=4)
		self.assertEqual(widget.get_template(), 'practice_test.html')
		widget = Widget(widget_type=5)
		self.assertEqual(widget.get_template(), 'writer_view.html')
		widget = Widget(widget_type=6)
		self.assertEqual(widget.get_template(), 'request_call.html')
		widget = Widget(widget_type=7)
		self.assertEqual(widget.get_template(), 'shine_ad.html')
		widget = Widget(widget_type=8)
		self.assertEqual(widget.get_template(), 'index_widget.html')

	def test_get_widget_data_method(self):
		widget = Widget(widget_type=1)
		data = widget.get_widget_data()
		self.assertIs('widget_type' in data.keys(), True)
		self.assertIs('heading' in data.keys(), True)
		self.assertIs('redirect_url' in data.keys(), True)
		self.assertIs('image' in data.keys(), True)
		self.assertIs('image_alt' in data.keys(), True)
		self.assertIs('description' in data.keys(), True)
		self.assertIs('document_upload' in data.keys(), True)
		self.assertIs('user' in data.keys(), True)
		self.assertIs('writer_designation' in data.keys(), True)
		self.assertIs('iw' in data.keys(), True)
		self.assertIs('is_external' in data.keys(), True)
		self.assertIs('is_pop_up' in data.keys(), True)
		self.assertIs('is_active' in data.keys(), True)

	def test_get_page_view(self):
		page = Page.objects.create(name='Resume For Experience', slug='resume-for-experience', is_active=True)
		response = self.client.get(page.get_absolute_url())
		self.assertEqual(response.status_code, 200)
		# request = self.factory.get(page.get_absolute_url())
		# request.user = AnonymousUser()
		# response = CMSPageView.as_view()(request)
		# self.assertEqual(response.status_code, 200)

	def test_post_page_view(self):
		page = Page.objects.create(name='Resume For Experience', slug='resume-for-experience', is_active=True)
		response = self.client.post(page.get_absolute_url(), {"message": "hello test", })
		comment_length = len(page.comment_set.all())
		self.assertEqual(comment_length, 0)
		self.assertRedirects(response, '/cms/page/resume-for-experience/')  # status code for redirection