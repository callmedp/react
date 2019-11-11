# python imports

import sys, os, django, pandas, json, logging

# Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
	sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

# django imports
from django.conf import settings

# local imports

from shop.models import Product, ProductScreen, Category
from assessment.models import Test, Question
from assessment.utils import VskillTest, VskillParser

ANSWER_MAPPING_DICT = {
	'a':'1',
	'b':'2',
	'c':'3',
	'd':'4',
	1  :'a',
	2  :'b',
	3  :'c',
	4  :'d',
	'A':'1',
	'B':'2',
	'C':'3',
	'D':'4',
}

if __name__ == "__main__":
	vskill_obj = VskillTest()
	vskill_parser = VskillParser()
	prodscreen_ids = vskill_obj.get_all_test_id()
	for product_id in prodscreen_ids:
		prodscreen = ProductScreen.objects.filter(id=product_id).first()
		if not prodscreen:
			logging.getLogger('info_log').info(
				'No Product Screen found for - {}'
				.format(product_id))
			continue
		prod = prodscreen.product
		if not prod:
			logging.getLogger('info_log').info(
				'No product found for product screen Id-{}'. \
				format(prodscreen.id))

		categories = list(prod.categories.all())
		# for parent categories decision is still pending change it accordingly

		category = Category.objects.filter(id=558).first()
		category = Category.objects.filter(id=83).first()
		if not category:
			continue
		categories.append(category)
		title = prod.name + '-' + str(prod.id)
		test_obj = Test.objects.create(product=prod, category=category,
									   duration=600,
									   title=title, is_active=True)
		if prod.vendor:
			test_obj.vendor = prod.vendor
		test_obj.save()
		test_obj.categories.set(categories)
		test_obj.save()

		vskill_parser.prepare_questions(vskill_obj.get_test_by_id(
			product_id), test_obj.id)













