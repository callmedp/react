from django_redis import get_redis_connection
from django.conf import settings
import os,sys,django,json



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

conn = get_redis_connection('search_lookup')

with open('data.json') as fp:
    data=json.load(fp)

conn.hmset('suggestion_set', data)








    