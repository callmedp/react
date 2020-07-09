import hashlib, base64
import logging, requests

from django.conf import settings
from django.core.cache import cache

from shop.models import Product, Category, AnalyticsVidhyaRecord
from partner.models import Vendor
from .choices import av_status_choices


class CourseCatalogueMixin(object):
	def get_course_catalogue_context(self):
		data = {}
		course_products = Product.browsable.filter(
			product_class__slug__in=settings.COURSE_SLUG,
			type_product__in=[0, 1]
		)

		fa_categories = Category.objects.filter(
			active=True, type_level=2).order_by('display_order')

		course_fa_categories = []
		for cat in fa_categories:
			if len(course_fa_categories) == 8:
				break

			skills = cat.to_category.filter(
				related_from__type_level__in=[3, 4], active=True,
				related_from__active=True,
				related_from__is_skill=True)
			if skills.exists():
				course_fa_categories.append(cat)

		course_fa_list = []
		for fa in course_fa_categories:
			fa_dict = {}
			icon = ''
			if fa.icon:
				icon = fa.icon.url
			elif fa.image:
				icon = fa.image.url
			fa_dict.update({
				"pk": fa.pk,
				"name": fa.name,
				"icon_image": icon,
				"url": fa.get_absolute_url()
			})

			course_fa_list.append(fa_dict)

			skills = fa.to_category.filter(
				related_from__type_level__in=[3, 4], active=True,
				related_from__active=True,
				related_from__is_skill=True).order_by('sort_order')[:5]
			skill_list = []
			for sk in skills:
				skill_dict = {}
				skill_dict.update({
					"pk": sk.related_from.pk,
					"name": sk.related_from.name,
					"url": sk.related_from.get_absolute_url()})

				skill_list.append(skill_dict)

				products = course_products.filter(
					categories=sk.related_from.pk).order_by('-buy_count')[: 4]

				product_list = []
				for pd in products:
					product_dict = {}
					product_dict.update({
						"pk": pd.pk,
						"name": pd.get_name,
						"url": pd.get_absolute_url()
					})
					product_list.append(product_dict)

				data.update({
					sk.related_from.pk: product_list
				})

			data.update({
				fa.pk: skill_list,
			})

		data.update({
			"course_fa_list": course_fa_list})

		vendor_list_ids = list(set(course_products.values_list('vendor', flat=True)))
		vendors = Vendor.objects.filter(
			id__in=vendor_list_ids).exclude(
			image__iexact='').order_by('priority')[: 4]
		vendor_list = []
		for v in vendors:
			v_dict = {}
			v_dict.update({
				"pk": v.pk,
				"name": v.name,
				"image": v.image.url, })
			vendor_list.append(v_dict)
		data.update({
			"vendor_list": vendor_list})

		cache.set(
			'course_catalogue',
			data, settings.COURSE_CATALOGUE_CASH_TIME)
		return data


class LinkedinSeriviceMixin(object):
	def validate_encrypted_key(self, token=None, email=None, prd=None):
		flag = False
		products_ids = []
		if token and email and prd:
			if prd in settings.LINKEDIN_RESUME_FREE:
				products_ids = settings.LINKEDIN_RESUME_FREE
			elif prd in settings.LINKEDIN_RESUME_COST:
				products_ids = settings.LINKEDIN_RESUME_COST
			else:
				products_ids = []

			for prd_id in products_ids:
				token_str = '{}pd-{}'.format(email, prd_id)
				gen_token = hashlib.sha256(
					token_str.encode()).hexdigest()
				if gen_token == token:
					flag = True
					break
		return flag

class AnalyticsVidhyaMixin(object):
	def get_api_header(self):
		username = settings.ANALYTICS_VIDHYA_URL.get('USERNAME', '')
		password = settings.ANALYTICS_VIDHYA_URL.get('PASSWORD', '')

		if not username and not password:
			return None

		us_pd = "{}:{}".format(username, password)
		b_us_pd = us_pd.encode('ascii')
		b64_us_pd = base64.b64encode(b_us_pd)
		b64_us_pd = b64_us_pd.decode('ascii')

		authorization = "Basic {}".format(b64_us_pd)

		headers = {"Authorization" : authorization}
		return headers

	def user_enrollment(self, data=None):
		if not data:
			logging.getLogger('error_log').error('data is empty')
			return False

		base_url = settings.ANALYTICS_VIDHYA_URL.get('BASE_URL', '')
		enrollment_url = settings.ANALYTICS_VIDHYA_URL.get('ENROLLMENT', '')

		url = base_url + enrollment_url
		headers = self.get_api_header()
		try:
			response = requests.post(url, data=data, headers=headers)
			if response.status_code == 201:
				logging.getLogger('info_log').info('request for user registeration \
					is successful')
			elif response.status_code == 401:
				logging.getLogger('error_log').error('something wrong with \
					authorization headers, contact Analytics Vidhya \
					for user - {}'.format(data))
				return False
			elif response.status_code == 400:
				error = response.json().get('errors')
				logging.getLogger('error_log').error('issue in json parsed \
					- {}'.format(error))
				return False
			else:
				logging.getLogger('error_log').error('something wrong with \
					response, contact Analytics Vidhya for user - {}'.format(data))
				return False
		except Exception as e:
			logging.getLogger('error_log').error('Unable to enroll the user,\
					please try again, user - {}'.format(data))
			return False

		data = response.json()
		status = data.get('status', '')
		product = data.get('product', {})
		if not av_status_choices.get(status) and not data.get('id') and not product:
	            logging.getLogger('error_log').error('invalid enrollment status or id or product')
	            return False

		data_dict = {
			'AV_Id' : data.get('id'),
			'name' : '{} {}'.format(data.get('first_name', ''), data.get('last_name', '')),
			'email' : data.get('email', ''),
			'phone' : data.get('phone_number', ''),
			'product_id' : product.get('id',''),
			'price' : data.get("price"),
			'price_currency' : data.get("price_currency"),
			'status' : 	av_status_choices.get(data.get('status')),
			'status_msg' : data.get('status_msg',''),
			'remarks' : data.get('remarks','')
		}
		try:
			user = AnalyticsVidhyaRecord.objects.create(**data_dict)
			if user:
				logging.getLogger("info_log").info("user is added in analytics vidhya record")
		except Exception as e:
			logging.getLogger("error_log").error("Unable to add record - {}".format(data_dict))
			return False
		return True



