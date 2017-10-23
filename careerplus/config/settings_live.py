from .settings import *

DEBUG = False
IS_LIVE = True
STATIC_URL = 'https://origin-static3.shine.com/'
########## DOMAIN SETTINGS ######################
MAIN_DOMAIN_PREFIX = 'http://learning1.shine.com'
SITE_DOMAIN = 'learning1.shine.com'
SITE_PROTOCOL = 'http'
SHINE_SITE = 'https://www.shine.com'
SHINE_API_URL = 'https://shine.com/api/v2'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

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

