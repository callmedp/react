from .settings import *
from .mongo.staging import *
from pymongo.read_preferences import ReadPreference

DEBUG = True
IS_LIVE = False
IS_GCP = True
ALLOWED_HOSTS = ['*']

####### DATABASE SETTINGS ###########
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

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

####### APPS SETTIMGS #################
DJANGO_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfaster',  # Needed here before staticfiles
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
if DEBUG:
    DEV_APPS = [
        'debug_toolbar',
        'rest_framework_swagger',
    ]
    INSTALLED_APPS += DEV_APPS

######### MIDDLEWARE SETTINGS ######
if DEBUG:
    DEV_MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
 #   MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG and not request.GET.get('nodebug'),
    'JQUERY_URL': '',

}

#### CELERY SETTINGS ########

########## WSGI SETTINGS #################
WSGI_APPLICATION = 'careerplus.config.wsgi.application'

INVOICE_DIR = 'invoice/'  # Cloud path
RESUME_DIR = 'resume/'  # Cloud path
RESUME_TEMPLATE_DIR = 'resume-builder'  # Cloud path

########## DOMAIN SETTINGS ######################
SITE_DOMAIN = 'learning1.shine.com'
MOBILE_SITE_DOMAIN = 'mlearning1.shine.com'
SITE_PROTOCOL = 'https'
# 'http://learning.shine.com'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)
MOBILE_PROTOCOL_DOMAIN = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)
META_SITE_PROTOCOL = SITE_DOMAIN
META_SITE_DOMAIN = SITE_PROTOCOL
META_FB_PROFILE_ID = '282244838633660'

######### SOLR SETTINGS #############
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        # prdt(staging learning1) # live_prod(staging learing2)
        'URL': 'http://172.22.67.214:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },

    'index': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        # prdt(staging learning1) # live_prod(staging learing2)
        'URL': 'http://172.22.67.214:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    }
}

###### SHINE SETTINGS ###########
SHINE_SITE = 'https://sumosc.shine.com'
SHINE_API_URL = 'https://sumosc.shine.com/api/v2'
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'tarun@123'
CLIENT_ACCESS_KEY = "ZiHCJeTKh4EppsrOEHXIQPd2OKvV4JWrlKql0Y1JONE"
CLIENT_ACCESS_SECRET = "QdEhIXFmhlHQdveZB1h9u9xxnfvFleET6bNUPlKYwU4"
SHINE_API_TIMEOUT = 5

# sumosc settings
SHINE_SITE = 'https://sumosc.shine.com'
SHINE_API_URL = 'https://sumosc.shine.com/api/v2'
CLIENT_ACCESS_KEY = "M2XFaFVHHJwlISEQxFQis1cQoKe6lIBKUGaEDG0WiHA"
CLIENT_ACCESS_SECRET = "aSQrGC9VZ866os5AZNGsor4CThxfGNz3s8V7rSMX3TY"
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'password'
SHINE_API_TIMEOUT = 5

CELERY_ALWAYS_EAGER = False

####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC49XECC'
CCAVENUE_WORKING_KEY = 'DE002F3C615C11E7FB7D333050103230'
CCAVENUE_MOBILE_ACCESS_CODE = 'AVYX74EK04AB50XYBA'
CCAVENUE_MOBILE_WORKING_KEY = 'A081DDE3B5B50F269F8980EB2ADEC9F3'
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'

####### EPAYLATER SETTINGS ###########################
EPAYLATER_INFO = {"payment_url": "https://payment-sandbox.epaylater.in/web/process-transaction",
                  "apiKey": "secret_31f23758-6325-442c-a98c-9eaf1d41a188",
                  "aeskey": "698042ECAE38D843A166AEFADD109687",
                  "iv": "D58C8D87960088FF",
                  "mCode": "SHINELEARNING",
                  "category": "LEARNING",
                  "base_url": "https://api-sandbox.epaylater.in/"}

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
    'candidate_search_lookup': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://172.22.67.223:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    },
    'job_title_lookup': {
        "BACKEND": "django_red.cache.RedisCache",
        "LOCATION": "redis://172.22.67.223:6379/13",
    },
    'token': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/12",
        "TIMEOUT": 30 * 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    }
}

###### LOGGING SETTINGS #############
SYSLOG_ADDRESS = '/dev/log'
# Following is to make sure logging works with mac machines 2
if sys.platform == "darwin":
    SYSLOG_ADDRESS = "/var/run/syslog"
# LOGGING['handlers']['syslog']['address'] = SYSLOG_ADDRESS

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
DEBUG = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

CART_DROP_OUT_EMAIL = 1
CART_DROP_OUT_LEAD = 3 * 60
SHIPPING_DROP_OUT_LEAD = 10 * 60
PAYMENT_DROP_LEAD = 5 * 60

# Booster Recruiters
BOOSTER_RECRUITERS = ['amar.kumar@hindustantimes.com']

CP_VENDOR_ID = '12345'

# ROUNDONE
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

# LINKEDIN SETTINGS
REDIRECT_URI = '{}/linkedin/login'.format(MAIN_DOMAIN_PREFIX)
CLIENT_ID = "757gbstpwa6dqp"
CLIENT_SECRET = "creqezZ0kPJnJWRk"
STATE = "9899002507upender"
SCOPE = 'r_emailaddress r_basicprofile'
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
OAUTH_URL = "https://www.linkedin.com/oauth/v2/authorization?"
LINKEDIN_INFO_API = "https://api.linkedin.com/v1/people/~:(id,first-name,last-name,picture-url,public-profile-url,email-address)?oauth2_access_token="
LINKEDIN_DICT = {
    "CLIENT_ID": "81fbxkgs5558q0",
    "CLIENT_SECRET": "ECioffWZKBbXhkbu",
}
TEST_EMAIL = True
TAG_MAILER = False

###### STORAGE SETTINGS #############
DEFAULT_FILE_STORAGE = 'core.library.gcloud.custom_cloud_storage.GCPMediaStorage'
GS_BUCKET_NAME = 'learning-media-staging-189607'

PRIVATE_MEDIA_FILE_STORAGE = 'core.library.gcloud.custom_cloud_storage.GCPPrivateMediaStorage'
GCP_PRIVATE_MEDIA_BUCKET = 'learning--misc-staging-189607'
GCP_RESUME_BUILDER_BUCKET = 'learning--misc-staging-189607'
CRM_PRIVATE_MEDIA_BUCKET = 'learningcrm-misc-staging-189607'

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
# new flow product
PORTFOLIO_PRODUCT_LIST = [2632, ]

# product list for linkedin resume services
LINKEDIN_RESUME_FREE = [2684, 2685]
LINKEDIN_RESUME_COST = [2682, 2683]
LINKEDIN_RESUME_PRODUCTS = LINKEDIN_RESUME_FREE + LINKEDIN_RESUME_COST

######## EMAIL SETTINGS ############
EMAIL_HOST = '172.22.65.228'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = 0
SERVER_EMAIL = 'learning@shine.com'
DEFAULT_FROM_EMAIL = CONSULTANTS_EMAIL
EMAIL_SERVER = 'http://localhost:8000'

###### SEARCH SETTINGS #######
EXCLUDE_SEARCH_PRODUCTS = LINKEDIN_RESUME_PRODUCTS

# used for coupon generation for free feature product on payment realization
FEATURE_PROFILE_PRODUCTS = [1939]

for conn, attrs in MONGO_SETTINGS.items():
    try:
        if attrs.get('REPSET'):
            connect(attrs['DB_NAME'],
                    host="mongodb://" +
                    attrs['USERNAME'] + ":" +
                    attrs['PASSWORD'] + "@" + attrs['HOST'],
                    maxPoolSize=attrs['MAX_POOL_SIZE'],
                    read_preference=ReadPreference.SECONDARY_PREFERRED,
                    replicaSet=attrs['REPSET'],
                    )
        else:
            connect(attrs['DB_NAME'],
                    host="mongodb://" + attrs['USERNAME'] + ":" + attrs['PASSWORD'] + "@" + attrs[
                        'HOST'] + "/?authSource=admin",
                    maxPoolSize=attrs['MAX_POOL_SIZE']
                    )
    except Exception as e:
        logging.getLogger('error_log').error(
            " unable to connect to mongo %s" % repr(e))
        continue


# test settings
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


TESTS_IN_PROGRESS = False
if 'test' in sys.argv[1:]:
    DEBUG = False
    TEMPLATE_DEBUG = False
    TESTS_IN_PROGRESS = True
    MIGRATION_MODULES = DisableMigrations()

########### CMS STATIC PAGE RENDERING ID#########

CMS_ID = [1]
FEATURE_PROFILE_EXCLUDE = [1941]
SERVICE_PAGE_ID_SLUG_MAPPING = {"45": "resume-writing"}
IS_MAINTENANCE = False
MAINTENANCE_MESSAGE = "This site will be under maintenance from 9 pm to 12 pm on Friday, 11 Jan, 2019."

# VIRTUAL_ENV PATH
VENV_PATH = "/root/virtualenvs/careerplus3.6/bin/python3"
CODE_PATH = "/code/careerplus/"

EXOTEL_DICT = {
    'token': '9e4df38c0c3bd1009ca142da306d827e71e74737',
    'sid': 'hindustantimes3',
    'callerid': '08047105151',
    'url': 'https://{sid}:{token}@api.exotel.com/v1/Accounts/{sid}/Calls/connect.json',
    'record_url': 'https://{sid}:{token}@api.exotel.com/v1/Accounts/{sid}/Calls/{callid}.json',
    'check_dnd_url': 'https://{sid}:{token}@api.exotel.com/v1/Accounts/{sid}/Numbers/{number}.json',
}

RESUME_BUILDER_NON_COMBO_PID = 3092
URL_SHORTENER_ACCESS_TOKEN = "29d325106d379436d7fbe9dc76844350859d24c1"
# Neo Settings
NEO_TOKEN = "xRm7FoiyQ221ZL7MV07zEOtcF3xrPcCTXYKmAnA5ylPtFWYCWJS6XqgXoHFsmuPR"
NEO_URL = {
    'pt_result': 'https://etestapi.dyned.com/pt/result',
    'board_user': 'https://universaldashboard.id.dyned.com/api/v1/student/onboard',
    'user_detail': 'https://universaldashboard.id.dyned.com/api/v1/student/',
    'jwt_token': 'https://myneo.space/api/v1/jwt/token-request',
    'get-sso-profile': 'https://myneo.space/api/v1/sso/user/{}/get/{}',
    'update-sso-profile': 'https://myneo.space/api/v1/dsa/admin/update-profile-sso/{}'
}
NEO_USERNAME = 'shineadmin@shine.com'
NEO_PASSWORD = 'MPgddK5vpM'

# Candidate Mongo Settings
CANDIDATE_MONGO_PORT = ':27017'
CANDIDATE_MONGO_USERNAME = 'candadmin'
CANDIDATE_MONGO_PASSWORD = 'candadmin'
CANDIDATE_MONGO_INSTANCE_STR = '172.22.67.226:27017'
CANDIDATE_MONGO_DB = 'sumoplus'
DEFAULT_RECOMMEND_PRODUCT = [2634, 2787]

try:
    from .settings_local import *
except:
    pass


# for testing purpose using live working key

# CCAVENUE_WORKING_KEY = 'BB84397177B2D640744BA272627C2A61'


CANDIDATE_SOLR_URL = "http://172.22.65.34:9999/solr/cda/select/"

RESUME_SHINE_SITE_PROTOCOL = 'https'
RESUME_SHINE_SITE_DOMAIN = 'resumestage.shine.com'
RESUME_SHINE_MAIN_DOMAIN = 'https://resumestage.shine.com'

'''
links for analytics vidhya 
'''
ANALYTICS_VIDHYA_URL = {
    'BASE_URL': 'https://id.aifest.org',
    'USERNAME': 'rajila.madhavan@hindustantimes.com',
    'PASSWORD': 'shine123',
    'ENROLLMENT': '/api/enrollments/requests',
    'STATUS': '/api/enrollments/requests/{}'
}
'''
link end
'''

PRODUCT_LEADCREATION_COUNTDOWN = 30


RESUME_SHINE_SITE_PROTOCOL = 'https'
RESUME_SHINE_SITE_DOMAIN = 'resumestage.shine.com'
RESUME_SHINE_MAIN_DOMAIN = '{}://{}'.format(RESUME_SHINE_SITE_PROTOCOL,RESUME_SHINE_SITE_DOMAIN)



CORS_ORIGIN_ALLOW_ALL = True
 
CORS_ORIGIN_WHITELIST = (
'https://localhost:8000',
'http://localhost:3000',
'https://127.0.0.1:8001',
'http://127.0.0.1:8000',
'https://learning2.shine.com',
'https://learning.shine.com',
'https://resume.shine.com',
 'https://learning1.shine.com',
 'https://resumestage.shine.com',
)
 
CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'token',
'access-key',
]
