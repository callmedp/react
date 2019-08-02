
#python imports

import sys,os,django,pandas

#Settings imports


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

from shop.models import Product
from assessment.models import Test,Question


if __name__ == "__main__":

    for file in os.listdir("/Users/gaurav/Desktop/20 files/"):
        product_id = file.split('_')[0]
        print(product_id)
        if not product_id.isnumeric():
            continue
        prod = Product.objects.filter(id=product_id).first()
        if not prod:
            continue

)
        category = prod.category_main
        df = pandas.read_excel("/Users/gaurav/Desktop/20 files/"+file)
        file_header = df.head(n=0)

        # test_obj = Test.objects.create(category=category,vendor=prod.vendor)
        for key in file_header[1:len(file_header)-1]:
            ques_op.update('')
     Question.objects.create(question_text=df[key][index])
