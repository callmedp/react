from .settings import *

DEBUG = True
IS_LIVE = False
IS_GCP = True

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
    'master': {
        'NAME': 'careerplus1',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },
    'slave': {
        'NAME': 'careerplus1',
        'ENGINE': 'django.db.backends.mysql',
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
DATABASE_ROUTERS = ['careerplus.config.db_routers.MasterSlaveRouter']


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

#### CELERY SETTINGS ########
BROKER_URL = 'redis://localhost:6379/0'

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
META_SITE_PROTOCOL = SITE_DOMAIN
META_SITE_DOMAIN = SITE_PROTOCOL
META_FB_PROFILE_ID = '282244838633660'


######### SOLR SETTINGS #############
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}

###### SHINE SETTINGS ###########
SHINE_SITE = 'https://sumosc.shine.com'
SHINE_API_URL = 'https://sumosc.shine.com/api/v2'
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'tarun@123'
CLIENT_ACCESS_KEY = "ZiHCJeTKh4EppsrOEHXIQPd2OKvV4JWrlKql0Y1JONE"
CLIENT_ACCESS_SECRET = "QdEhIXFmhlHQdveZB1h9u9xxnfvFleET6bNUPlKYwU4"
SHINE_API_TIMEOUT = 5

CELERY_ALWAYS_EAGER = False


####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC49XECC'
CCAVENUE_WORKING_KEY = 'DE002F3C615C11E7FB7D333050103230'
CCAVENUE_MOBILE_ACCESS_CODE = 'AVYX74EK04AB50XYBA'
CCAVENUE_MOBILE_WORKING_KEY = 'A081DDE3B5B50F269F8980EB2ADEC9F3'
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'

###### CACHE SETTINGS #################
SITEMAP_CACHING_TIME = 86400
# Cache related settings
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:6379/1",
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
            "redis://127.0.0.1:6379/2",
            ],
        "TIMEOUT": 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.ShardClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    },
    'search_lookup': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    },
}


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

CART_DROP_OUT_EMAIL = 1 * 60
CART_DROP_OUT_LEAD = 3 * 60
SHIPPING_DROP_OUT_LEAD = 10 * 60
PAYMENT_DROP_LEAD = 5 * 60

# Booster Recruiters
BOOSTER_RECRUITERS = ['amar.kumar@hindustantimes.com']

CP_VENDOR_ID = '12345'

##### ROUNDONE
ROUNDONE_PRODUCT_ID = 2129
ROUNDONE_API_BASEURL = "http://api.roundone.asia"
ROUNDONE_API_BASEURL_ORDER = "http://testing.roundone.asia"
ROUNDONE_ORDER_SECRET_KEY = 'xHVEbrvpiH8BMol5rZt7YuDO'
ROUNDONE_JOBDETAIL_SECRET_KEY = 'cQMYGVYxrMqHGPSAZeRDm4G'
ROUNDONE_CP_CLIENT_ID = 'lnVPB3Oe9YPA3g)!F9zrFbg'
ROUNDONE_CP_CLIENT_SECRET = 'c&OMxZ^0T*6qvyi0e3lU9OjWc!(%Wp+'
ROUNDONE_ENCODING_KEY = 'roundonetestkey'
ROUNDONE_ENCODING_SALT = 'roundonetestsalt'
ROUNDONE_DEFAULT_PASSWORD = 'cp@roundone'
ROUNDONE_API_TIMEOUT = 5
ROUNDONE_API_DICT = {
    'amount': 1999,
    'organisationId': 11,
    'affiliateName': 'CP',
    'client_id': ROUNDONE_CP_CLIENT_ID,
    'client_secret': ROUNDONE_CP_CLIENT_SECRET,
    'order_secret_key': ROUNDONE_ORDER_SECRET_KEY,
    'jobdetail_secret_key': ROUNDONE_JOBDETAIL_SECRET_KEY,
    'location_url': ROUNDONE_API_BASEURL + "/applicant/location-list",
    'order_save_url': ROUNDONE_API_BASEURL_ORDER + "/api/careerplus/save",
    'job_search_url': ROUNDONE_API_BASEURL + "/applicant/search",
    'oauth_url': ROUNDONE_API_BASEURL + "/oauth-token",
    'job_detail_url': ROUNDONE_API_BASEURL + "/applicant/job-details",
    'is_premium_url': ROUNDONE_API_BASEURL + "/applicant/is-premium",
    'save_job_url': ROUNDONE_API_BASEURL + "/applicant/save-jobs",
    'get_profile_url': ROUNDONE_API_BASEURL + "/applicant/get-profile",
    'post_profile_url': ROUNDONE_API_BASEURL + "/applicant/post-profile",
    'submit_resume': ROUNDONE_API_BASEURL + "/applicant/submit-resume",
    'referral_request_url': ROUNDONE_API_BASEURL + "/applicant/referral-request",
    'referral_status_url': ROUNDONE_API_BASEURL + "/applicant/referral-status",
    'referral_confirm_url': ROUNDONE_API_BASEURL + "/applicant/confirm-interaction",
    'upcoming_interaction_url': ROUNDONE_API_BASEURL + "/applicant/upcoming-interactions",
    'past_interaction_url': ROUNDONE_API_BASEURL + "/applicant/past-interactions",
    'saved_history_url': ROUNDONE_API_BASEURL + "/applicant/get-saved-jobs",
    'delete_job_url': ROUNDONE_API_BASEURL + "/applicant/delete-saved-job",
    'feedback_submit_url': ROUNDONE_API_BASEURL + "/applicant/submit-feedback",
    'interaction_result_url': ROUNDONE_API_BASEURL + "/applicant/view-interaction-result",
    'update_credential_url': ROUNDONE_API_BASEURL + "/applicant/update-credentials"
}

### LINKEDIN SETTINGS
REDIRECT_URI = '{}/linkedin/login'.format(MAIN_DOMAIN_PREFIX)
CLIENT_ID = "815g8q57sg0q6q"
CLIENT_SECRET = "NljH5Pdr6e80MTuR"
STATE = "9899002507upender"
SCOPE = 'r_emailaddress r_basicprofile'
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
OAUTH_URL = "https://www.linkedin.com/oauth/v2/authorization?"
LINKEDIN_DICT = {
    "CLIENT_ID": "81fbxkgs5558q0",
    "CLIENT_SECRET": "ECioffWZKBbXhkbu",
}

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
STATIC_URL = 'https://{}.storage.googleapis.com/l/s/'.format(GCP_STATIC_BUCKET)
MEDIA_URL = 'https://{}.storage.googleapis.com/l/m/'.format(GS_BUCKET_NAME)

# Addon List For writer Invoice
VISUAL_RESUME_PRODUCT_LIST = [305, 306, 307, 308, 309]
COVER_LETTER_PRODUCT_LIST = [83, ]
SECOND_REGULAR_RESUME_PRODUCT_LIST = [126, 127, 128, 129, 130]

# product list for linkedin resume services
LINKEDIN_RESUME_FREE = []
LINKEDIN_RESUME_COST = [2682, 2683]
LINKEDIN_RESUME_PRODUCTS = LINKEDIN_RESUME_FREE + LINKEDIN_RESUME_COST

########## CRM SETTINGS #############
SHINECPCRM_DICT = {
    'base_url': 'http://172.22.65.32:8003',
    'token': '73f53cf358b94156feb49d034081ed507334e02a',
    'create_lead_url': '/api/v1/create-lead/',
    'update_products_url': '/product/update_sale_product/',
    'update_cartleads_url': '/api/update-cartleads/',
    'ad_server_url': '/api/mobile-version-leads/',
    'timeout': 30,
}

######## EMAIL SETTINGS ############
EMAIL_HOST = '172.22.65.188'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = 0
SERVER_EMAIL = 'recruiter@shine.com'
DEFAULT_FROM_EMAIL = CONSULTANTS_EMAIL
EMAIL_SERVER = 'http://localhost:8000'

try:
    from .settings_local import *
except:
    pass
