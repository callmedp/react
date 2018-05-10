import hashlib

from django.conf import settings
from django.core.cache import cache

from shop.models import Product, Category
from partner.models import Vendor


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
