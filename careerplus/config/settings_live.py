from .settings import *

DEBUG = False
IS_LIVE = True
STATIC_URL = 'https://origin-static3.shine.com/static/'
MEDIA_URL = 'https://origin-static3.shine.com/'
########## DOMAIN SETTINGS ######################
SITE_DOMAIN = 'learning.shine.com'
MOBILE_SITE_DOMAIN = 'm-learning.shine.com'
SITE_PROTOCOL = 'https'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN) #'http://learning.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'tarun@123'
SHINE_API_TIMEOUT = 60
SHINE_SITE = 'https://www.shine.com'
SHINE_API_URL = 'https://mapi.shine.com/api/v2'
CLIENT_ACCESS_KEY = 'ZiHCJeTKh4EppsrOEHXIQPd2OKvV4JWrlKql0Y1JONE'
CLIENT_ACCESS_SECRET = 'QdEhIXFmhlHQdveZB1h9u9xxnfvFleET6bNUPlKYwU4'

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.36:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
    'index': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.35:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    }
}

####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC48XECC'
CCAVENUE_WORKING_KEY = 'BB84397177B2D640744BA272627C2A61'
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerplus',
        'USER': 'carrerplus',
        'PASSWORD': 'permitted@321',
        'HOST': '172.22.65.153',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://172.22.65.131:6379/1",
            ],
        "TIMEOUT": 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    },
    'session': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://172.22.65.131:6379/2",
            "redis://172.22.65.141:6379/2",
            ],
        "TIMEOUT": 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    },
    'search_lookup': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.22.65.131:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    },
}

ADMINS = [
    '123snig@gmail.com',
    'snig_b@yahoo.com'
    'snigdha.batra@hindustantimes.com'
]

ROUNDONE_PRODUCT_ID = 2129
