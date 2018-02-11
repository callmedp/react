from .settings import *

DEBUG = True
IS_LIVE = False

ALLOWED_HOSTS = ['*']

######## DATABASE SETTINGS ###########
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerplus1',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },

    'oldDB': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shinecp',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },
}


####### APPS SETTIMGS #################
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfaster',       # Needed here before staticfiles
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
if DEBUG:
    DEV_APPS = [
        'debug_toolbar'
    ]
    INSTALLED_APPS += DEV_APPS

######### MIDDLEWARE SETTINGS ######
if DEBUG:
    DEV_MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE


########## WSGI SETTINGS #################
WSGI_APPLICATION = 'careerplus.config.wsgi.application'

INVOICE_DIR = 'invoice/'   # Cloud path
RESUME_DIR = 'resume/'  # Cloud path

########## DOMAIN SETTINGS ######################
SITE_DOMAIN = 'learning1.shine.com'
MOBILE_SITE_DOMAIN = 'mlearning1.shine.com'
SITE_PROTOCOL = 'https'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)  #'http://learning.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}

SHINE_SITE = 'https://sumosc.shine.com'
SHINE_API_URL = 'https://sumosc.shine.com/api/v2'

CELERY_ALWAYS_EAGER = False


####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC49XECC'
CCAVENUE_WORKING_KEY = 'DE002F3C615C11E7FB7D333050103230'

##### CCAVENUE MOBILE SETTINGS ###########
CCAVENUE_MOBILE_ACCESS_CODE = 'AVYX74EK04AB50XYBA'
CCAVENUE_MOBILE_WORKING_KEY = 'A081DDE3B5B50F269F8980EB2ADEC9F3'

CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'



###### CACHE SETTINGS #################
SITEMAP_CACHING_TIME = 86400

###### LOGGING SETTINGS #############
SYSLOG_ADDRESS = '/dev/log'
# Following is to make sure logging works with mac machines 2
if sys.platform == "darwin":
    SYSLOG_ADDRESS = "/var/run/syslog"
LOGGING['handlers']['syslog']['address'] = SYSLOG_ADDRESS

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
DEBUG = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
IS_LIVE = False

CART_DROP_OUT_EMAIL = 1 * 60
CART_DROP_OUT_LEAD = 3 * 60
SHIPPING_DROP_OUT_LEAD = 10 * 60
PAYMENT_DROP_LEAD = 5 * 60

try:
    from .settings_local import *
except:
    pass

##### ROUNDONE
ROUNDONE_PRODUCT_ID = 2129

### LINKEDIN SETTINGS
REDIRECT_URI = '{}/linkedin/login'.format(MAIN_DOMAIN_PREFIX)


###### STORAGE SETTINGS #############
DEFAULT_FILE_STORAGE = 'core.library.gcloud.custom_cloud_storage.GCPMediaStorage'
GS_BUCKET_NAME = 'learning-media-staging-189607'

PRIVATE_MEDIA_FILE_STORAGE = 'core.library.gcloud.custom_cloud_storage.GCPPrivateMediaStorage'
GCP_PRIVATE_MEDIA_BUCKET = 'learning--misc-staging-189607'

COMPRESS_STORAGE = STATICFILES_STORAGE = 'core.library.gcloud.custom_cloud_storage.GCPStaticStorage'
GS_PROJECT_ID = 'shine-staging-189607'
GCP_STATIC_BUCKET = 'learning-static-staging-189607'

INVOICE_FILE_STORAGE = 'core.library.gcloud.custom_cloud_storage.GCPInvoiceStorage'
GCP_INVOICE_BUCKET = 'learning-invoices-staging-189607'

# GS_AUTO_CREATE_BUCKET = True
STATIC_URL = 'https://{}.storage.googleapis.com/'.format(GCP_STATIC_BUCKET)
MEDIA_URL = 'https://{}.storage.googleapis.com/'.format(GS_BUCKET_NAME)
