import hashlib, base64
import logging, requests

from django.conf import settings
from django.core.cache import cache
from datetime import datetime

from shop.models import Product, Category,Skill
from partner.models import Vendor
from django.core.mail import EmailMessage
from order.models import AnalyticsVidhyaRecord
from partner.models import ProductSkill


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



class SkillProducts:


	def get_value_products(self,fl=[],products=[]):
		data = []
		fl_mapping = {
			'id': 'id',
			'title':'title',
			'vendor_id': 'vendor_id',
			'fake_inr_price': 'fake_inr_price',
		}

		fl_func_mapping = {
			'heading': 'get_heading',
			# 'title': 'get_title',
			'icon': 'get_icon_url',
			'url':  'get_url',
			'about': 'get_about',
			'inr_price': 'get_price',
			'attribute': 'get_assessment_attribute',
			'img_url': 'get_image_url',
			'vendor_name': 'get_vendor'
		}
		WhatYouGet = {
			'testpreptraining': [
				"Receive valuable feedback, from reliable exam reports, on your strong and weak areas",
				"Get real exam and practice environment",
				"In depth and exhaustive explanation to every question to enhance your learning",
				"Unlimited access to the assessment platform",
				"500+ questions to test your learning on variety of topics",
				"Gets Tips & Tricks to crack the test",
			],
		}

		for prod in products:
			data_dict = {}

			for f in fl:
				if f in fl_mapping.keys():
					data_dict.update({f: getattr(prod,fl_mapping[f],None)})
				if f in fl_func_mapping.keys():
					if fl_func_mapping.get(f):
						data_dict.update({f:getattr(prod,fl_func_mapping[f])()})
					else:
						data_dict.update({f:''})
			if fl:
				data.append(data_dict)
				continue

			data_dict.update({'id': prod.id, 'heading': prod.get_heading(), 'title': prod.get_title(),
							  'url': prod.get_url(),
							  'icon': prod.get_icon_url(), 'about': prod.get_about(),
							  'img_url': prod.image.url if prod.image else '',
							  'inr_price': prod.get_price(),
							  'vendor_'
							  'fake_inr_price': prod.fake_inr_price, 'attribute': prod.get_assessment_attribute(),
							  'vendor': prod.vendor_id})

			if prod.type_flow == 16:
				if not prod.vendor:
					data_dict.update({
						'what_you_get': [
							"Industry recognized certification after clearing the test",
							"Get badge on shine.com and showcase your knowledge to the recruiters",
							"Shine shows your skills as validated and certification as verified which build high trust "
							"among recruiters",
							"Receive valuable feedback on your strong and weak areas to improve yourself",
							"Certified candidates gets higher salary as compared to non certified candidate"
						]
					})
				else:
					data_dict.update({
						'what_you_get': WhatYouGet.get(prod.vendor.slug, [
							"Industry recognized certification after clearing the test",
							"Get badge on shine.com and showcase your knowledge to the recruiters",
							"Shine shows your skills as validated and certification as verified which build high trust "
							"among recruiters",
							"Receive valuable feedback on your strong and weak areas to improve yourself",
							"Certified candidates gets higher salary as compared to non certified candidate"
						])
					})

			data.append(data_dict)
		return data



	def get_product_from_skill(self, skill=[], fl=[]):
		if not skill:
			return []
		filter_dict = {'active': True, 'is_indexed': True, 'is_indexable': True}
		product_id = None
		assessment = self.request.GET.get('assessment')

		if assessment:
			filter_dict.update({'type_flow': 16})



		if isinstance(skill, list):
			product_id = ProductSkill.objects.filter(skill__slug__in=skill).values_list('product_id', flat=True)

		else:
			product_id = ProductSkill.objects.filter(skill__slug=skill).values_list('product_id', flat=True)


		if  'vendor_name' in fl:

			products = Product.objects.select_related('vendor').filter(id__in=product_id, **filter_dict).order_by(
				'-vendor__priority')
		else:
			products = Product.objects.filter(id__in=product_id, **filter_dict).order_by(
				'-vendor__priority')

		return self.get_value_products(fl,products)


	def get_all_products_with_skill(self,specific_vendor = []):
		data = []
		skill_to_product_map = {}
		vendor_to_product_map = {}
		vendor_id_to_name_map = {}
		skill_id_to_skill_name={}
		prod_id_to_details = {}

		pdlist = Product.objects.values_list('id','title', 'vendor_id','vendor__name')
		for pdl in pdlist:
			prod_id_to_details[pdl[0]] = {
				'title': pdl[1],
				'vendor_id': pdl[2],
				'vendor_name':pdl[3],
				'id':pdl[0],
			}

		ps = ProductSkill.objects.values('skill_id','product_id')

		for i in ps:
			val = skill_to_product_map.get(i.get('skill_id',[]),[])
			val.append(i.get('product_id',-1))
			skill_to_product_map[i['skill_id']] = val

		for i in Skill.objects.values('id','slug'):
			skill_id_to_skill_name[i['id']] = i['slug']

		for i in Vendor.objects.values('id','name'):
			vendor_id_to_name_map[i['id']] = i['name']

		product_ids = [y for x in skill_to_product_map.values() for y in x]

		products = Product.objects.filter(id__in=product_ids)

		for prod in products:
			val = vendor_to_product_map.get(prod.vendor_id,[])
			val.append(prod.id)
			vendor_to_product_map[prod.vendor_id] = val
		vendors = vendor_to_product_map.keys()
		vendors = list(Vendor.objects.filter(id__in=vendors).order_by('-priority').values_list('id',flat=True))
		if specific_vendor:
			vendors = specific_vendor

		new_data = {}

		for sk, prod in skill_to_product_map.items():
			skill_products = []
			for vendor in vendors:
				prd = list(set(vendor_to_product_map[vendor]).intersection(set(skill_to_product_map[sk])))
				if not prd:
					continue
				skill_products = skill_products + prd
			skill_products = [prod_id_to_details.get(i) for i in skill_products]
			new_data[skill_id_to_skill_name[sk]] = skill_products

		return new_data











			







