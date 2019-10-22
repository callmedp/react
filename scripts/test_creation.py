
#python imports

import sys,os,django,pandas,json,logging

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
	sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports
from django.conf import settings


#local imports

from shop.models import Product,ProductScreen
from assessment.models import Test,Question

ANSWER_MAPPING_DICT = {
	'a': '1',
	'b': '2',
	'c': '3',
	'd': '4',
	1:   'a',
	2:    'b',
	3:    'c',
	4:    'd',
	'A': '1',
	'B': '2',
	'C': '3',
	'D': '4',
}

if __name__ == "__main__":
	for file in os.listdir("/Users/gaurav/Desktop/test_prep/"):
		product_id = file.split('_')[0]
		if not product_id.isnumeric():
			continue
		prodscreen = Product.objects.filter(id=product_id).first()
		if not prodscreen:
			logging.getLogger('info_log').info('No Product found for - {}'.format(product_id))
			continue
		if not prodscreen:
			logging.getLogger('info_log').info('No product found for product screen Id-{}'.\
											   format(prodscreen.id))
		prod= prodscreen
		category = prod.category_main
		df = pandas.read_excel("/Users/gaurav/Desktop/test_prep/"+file,
							   dtype=str)
		logging.getLogger('info_log').info('Reading File  - {}'.format(file))
		title = prod.name+'-'+str(prod.id)
		test_obj = Test.objects.create(product=prod,duration=600,title=title,is_active=True)
		if category:
			test_obj.category = category
		if prod.vendor:
			test_obj.vendor = prod.vendor
		test_obj.save()
		for question_array in df.get_values()[:df.values.size]:
			question_object = Question.objects.create()
			question_dict = {}
			option_list = []
			question_dict.update({'test': test_obj})
			if len(question_array[-1]) > 1:
				question_dict.update({'question_type': 2})
			for index, value in enumerate(question_array[:-1]):
				option_dict = {}
				if index == 0:
					question_dict.update({'question_text': value})
					continue
				if str(index) in list(map(lambda x : x.strip(),
										  question_array[-1].split(','))):
					option_dict.update({'is_correct': '1'})
				else:
					option_dict.update({'is_correct': '0'})
				option_dict.update({'option': value, 'option_id': str(question_object.id) +
									ANSWER_MAPPING_DICT.get(index), 'option_image': ''})
				option_list.append(option_dict)
			option_json = json.dumps(option_list)

			question_dict.update({'question_options': option_json})
			for key,value in question_dict.items():
				setattr(question_object,key,value)
			question_object.save()
			print(test_obj.id)
			logging.getLogger('info_log').info('Question Object Created - {}'.format(question_object.id))