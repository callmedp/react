#python imports

#django imports

#local imports
from .base_settings import *  # noqa
from .celery import *

#inter app imports

#third party imports
from pymongo import read_preferences
from mongoengine import connect

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_LIVE = False
IS_GCP = False
ALLOWED_HOSTS = ['*']


####### CACHE SETTINGS ##############
SITEMAP_CACHING_TIME = 1

#### Database SETTINGS ######f########
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerplus_test',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },
    'master': {
        'NAME': 'careerplus_test',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },
    'slave': {
        'NAME': 'careerplus_test',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },
    # 'oldDB': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'shinecp',
    #     'USER': 'root',
    #     'PASSWORD': 'root',
    #     'HOST': '',
    #     'PORT': '',
    # },
}

DATABASE_ROUTERS = ['careerplus.config.db_routers.MasterSlaveRouter']

######### Apps specific for this project go here. ###########
DJANGO_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'collectfaster',       # Needed here before staticfiles
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DEV_APPS = [
    'debug_toolbar',
    'rest_framework_swagger',
]
INSTALLED_APPS += DEV_APPS


####### MIDDLEWARE SETTINGS #####################
DEV_MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]
MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : lambda request: DEBUG and not request.GET.get('nodebug'),
    'ENABLE_STACKTRACES_LOCALS': True,
    'SHOW_COLLAPSED': True
    
}

#### CELERY SETTINGS ########
BROKER_URL = 'redis://localhost:6379/0'

####### WSGI SETTINGS ############
WSGI_APPLICATION = 'careerplus.config.wsgi.application'


INTERNAL_IPS = ('127.0.0.1',)

SITE_DOMAIN = '127.0.0.1:8000'
MOBILE_SITE_DOMAIN = 'm-learn.shine.com:8007'
SITE_PROTOCOL = 'http'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)  #'http://learning.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)

META_SITE_PROTOCOL = SITE_DOMAIN
META_SITE_DOMAIN = SITE_PROTOCOL
# META_FB_APPID = '1482454715170390'
META_FB_PROFILE_ID = '282244838633660'
# META_FB_PUBLISHER = 'https://facebook.com/foo.blag'
# META_FB_AUTHOR_URL = 'https://facebook.com/foo.blag'
# META_TWITTER_TYPE = 'summary_large_image'
# META_TWITTER_SITE = '@FooBlag'
# META_TWITTER_AUTHOR = '@FooBlag'
# META_GPLUS_AUTHOR = '+FooBar'


####### ROUNDONE SETTINGS ##########
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
ROUNDONE_PRODUCT_ID = 2129

####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC49XECC'
CCAVENUE_WORKING_KEY = 'DE002F3C615C11E7FB7D333050103230'

####### EPAYLATER SETTINGS ###########################
EPAYLATER_INFO = {"payment_url":"https://payment-sandbox.epaylater.in/web/process-transaction",
                "apiKey": "secret_31f23758-6325-442c-a98c-9eaf1d41a188",
                "aeskey": "698042ECAE38D843A166AEFADD109687",
                "iv": "D58C8D87960088FF",
                "mCode": "SHINELEARNING",
                "category" : "LEARNING",
                "base_url":"https://api-sandbox.epaylater.in/"}

# Shine settings

SHINE_SITE = 'https://www.shine.com'
SHINE_API_URL = 'https://mapi.shine.com/api/v2'
CLIENT_ACCESS_KEY = "ZiHCJeTKh4EppsrOEHXIQPd2OKvV4JWrlKql0Y1JONE"
CLIENT_ACCESS_SECRET = "QdEhIXFmhlHQdveZB1h9u9xxnfvFleET6bNUPlKYwU4"
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'tarun@123'
SHINE_API_TIMEOUT = 5

# sumosc settings
SHINE_SITE = 'https://sumosc.shine.com'
SHINE_API_URL = 'https://sumosc.shine.com/api/v2'
CLIENT_ACCESS_KEY = "M2XFaFVHHJwlISEQxFQis1cQoKe6lIBKUGaEDG0WiHA"
CLIENT_ACCESS_SECRET = "aSQrGC9VZ866os5AZNGsor4CThxfGNz3s8V7rSMX3TY"
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'password'
SHINE_API_TIMEOUT = 5

########## CRM SETTINGS #############
SHINECPCRM_DICT = {
    'base_url': 'http://shinecpcrm1.shine.com',
    'token': '73f53cf358b94156feb49d034081ed507334e02a',
    'create_lead_url': '/api/v1/create-lead/',
    'update_products_url': '/product/update_sale_product/',
    'update_cartleads_url': '/api/update-cartleads/',
    'ad_server_url': '/api/mobile-version-leads/',
    'connected_leads': '/api/orders/order-fetch-lead/',
    'timeout': 30,
}


# Email settings

# VARIABLE FOR SENDING RESUME SERVICES MAILS
CANDIDATES_EMAIL = 'Shine.com <candidates@shine.com>'

EMAIL_HOST = '172.22.65.228'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = 0
SERVER_EMAIL = 'learning@shine.com'
DEFAULT_FROM_EMAIL = CONSULTANTS_EMAIL
EMAIL_SERVER = 'http://localhost:8000'

# Linkedin Credentials
CLIENT_ID = "815g8q57sg0q6q"
CLIENT_SECRET = "NljH5Pdr6e80MTuR"

REDIRECT_URI = '{}/linkedin/login'.format(MAIN_DOMAIN_PREFIX)
STATE = "9899002507upender"
SCOPE = 'r_emailaddress r_basicprofile'
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
OAUTH_URL = "https://www.linkedin.com/oauth/v2/authorization?"
LINKEDIN_INFO_API="https://api.linkedin.com/v1/people/~:(id,first-name,last-name,picture-url,public-profile-url,email-address)?oauth2_access_token="

LINKEDIN_DICT = {
    "CLIENT_ID": "81fbxkgs5558q0",
    "CLIENT_SECRET": "ECioffWZKBbXhkbu",
}

# Cart Drop Out Set Time For Task
CART_DROP_OUT_EMAIL = 1 * 60
CART_DROP_OUT_LEAD = 3 * 60
SHIPPING_DROP_OUT_LEAD = 10 * 60
PAYMENT_DROP_LEAD = 5 * 60

# Booster Recruiters
BOOSTER_RECRUITERS = ['amar.kumar@hindustantimes.com']

CP_VENDOR_ID = '12345'

############ SOLR SETTINGS #######################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.67.244:8983/solr/prdt',  # prdt(staging learning1) # live_prod(staging learing2)
        'INCLUDE_SPELLING': False,
    },

    'index': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.67.244:8983/solr/prdt',  # prdt(staging learning1) # live_prod(staging learing2)
        'INCLUDE_SPELLING': False,
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

############# REDIS SETTINGS ###################
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
    'test_lookup': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": ["redis://localhost:6379/1"],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
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

    'search_lookup': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    },
    'token': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "TIMEOUT": 30 * 86400,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        }
    }
}


######## LOGGING SETTINGS ##########
SYSLOG_ADDRESS = '/dev/log'
# Following is to make sure logging works with mac machines 2
if sys.platform == "darwin":
    SYSLOG_ADDRESS = "/var/run/syslog"
LOGGING['handlers']['syslog']['address'] = SYSLOG_ADDRESS


######## STORAGE SETTINGS #############
GS_BUCKET_NAME = 'learning-media-staging-189607'
GCP_PRIVATE_MEDIA_BUCKET = 'learning--misc-staging-189607'
GCP_STATIC_BUCKET = 'learning-static-staging-189607'
GCP_INVOICE_BUCKET = 'learning-invoices-staging-189607'
GCP_RESUME_BUILDER_BUCKET = 'learning--misc-staging-189607'

# Addon List For writer Invoice
VISUAL_RESUME_PRODUCT_LIST = [305, 306, 307, 308, 309]
COVER_LETTER_PRODUCT_LIST = [83, ]
SECOND_REGULAR_RESUME_PRODUCT_LIST = [126, 127, 128, 129, 130]
# new flow product
PORTFOLIO_PRODUCT_LIST = [2632, ]

EXECUTIVE_BIO_PRODUCT_LIST = [2051]

# product list for linkedin resume services
LINKEDIN_RESUME_FREE = [2684, 2685]
LINKEDIN_RESUME_COST = [2682, 2683]
LINKEDIN_RESUME_PRODUCTS = LINKEDIN_RESUME_FREE + LINKEDIN_RESUME_COST

###### SEARCH SETTINGS #######
EXCLUDE_SEARCH_PRODUCTS = LINKEDIN_RESUME_PRODUCTS

######### CONTACT NUMBERS ###################

GGN_CONTACT_FULL = '0124-6096096/97'
GGN_CONTACT = '0124-6096096'
TOLL_FREE_NUMBER = '18005727007'
MISSED_CALL_NUMBER = '08047106646'

########### CMS STATIC PAGE RENDERING ID#########

CMS_ID = [1]

# used for coupon generation for free feature product on payment realization
FEATURE_PROFILE_PRODUCTS = [1939]

SERVICE_PAGE_ID_SLUG_MAPPING = {"45":"resume-writing"}
#whatsapp jobs list products
FEATURE_PROFILE_EXCLUDE=[49]
TEST_EMAIL = False


VENDOR_URLS = {
    'amcat': {
        'all_certificates': 'https://www.myamcat.com/api/3p/assessment-results',
        'get_autologin_url': 'https://www.myamcat.com/api/3p/schedule-skill-test'
    }
}


AMCAT_API_TOKEN = '7347D18D79F6431CB9ACADBE704B2389'
AMCAT_API_SECRET = '7B348DF7F1A4EBED5DCBC0A1E4AC6B67'

IMPORT_CERTIFICATE_ALLOWED_VEDOR = ('amcat','testprep')

EXOTEL_DICT = {
           'token': '9e4df38c0c3bd1009ca142da306d827e71e74737',
           'sid': 'hindustantimes3',
           'callerid': '08047105151',
           'url': 'https://{sid}:{token}@api.exotel.com/v1/Accounts/{sid}/Calls/connect.json',
           'record_url': 'https://{sid}:{token}@api.exotel.com/v1/Accounts/{sid}/Calls/{callid}.json',
           'check_dnd_url': 'https://{sid}:{token}@api.exotel.com/v1/Accounts/{sid}/Numbers/{number}.json',
            }

RESUME_BUILDER_NON_COMBO_PID = 3092
URL_SHORTENER_AUTH_DICT = {"access_token":"29d325106d379436d7fbe9dc76844350859d24c1",
                        "end_point":"https://u.shine.com/api/generate-url/"
                        }

WHATS_APP_MESSAGE_FORMAT = '''Here are our job recommendations for this week.<br>
                        <br>{}Please do not call/reply directly to this message<br><br>In case of any queries, you can call us on  08047105151 or email us at resume@shine.com<br><br>Thanks,<br><br>Team Shine
                        '''

ROOT_URLCONF = 'careerplus.config.urls'
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

LOGGED_IN_CHATBOT = "https://static1.shine.com/l/cm/chatbot/learning_learning_logged_in-1601875262.js"
NON_LOGGED_IN_CHATBOT = "https://static1.shine.com/l/cm/chatbot/learning_learning_nonloggedin-1601875610.js"

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'print preview importcss searchreplace autolink autosave save directionality \
                visualblocks visualchars fullscreen image link media template codesample code table charmap hr \
                pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars\
                emoticons blockquote',
    'cleanup_on_startup': True,
    'menubar': 'file edit view insert format tools table help',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright \
        alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak\
        | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample code | a11ycheck ltr rtl\
        | showcomments addcomment toc | blockquote',
    'custom_undo_redo_levels': 6,
    'toolbar_mode': 'sliding',
}

RESUME_SHINE_URL = "https://resume.shine.com"
PAGINATOR_PAGE_SIZE = 10

#recommendation engine apis
ANALYTICS_COURSES_RECOMMENDATION_API = "http://10.136.1.4:5000/courses"
ANALYTICS_COURSES_RECOMMENDATION_API_AUTH = ("admin", "learningcourse@111")

#Recommendation Learning Mongo Database connections details
ANALYTICS_MONGO_PORT = ':27017'
ANALYTICS_MONGO_USERNAME = 'analyticsTeam'
ANALYTICS_MONGO_PASSWORD = '@n@lyt!c$'
ANALYTICS_MONGO_INSTANCE_STR = '172.22.65.150:27017'
ANALYTICS_MONGO_DB = 'analyticsLearning'

#Default products to be recommended
DEFAULT_LEARNING_COURSE_RECOMMENDATION_PRODUCT_ID = [2634, 2787, 1, 4]
DEFAULT_LEARNING_SERVICE_RECOMMENDATION_CANDIDATE_ID = '000000000000000000000000'

# product of Resume Critique flow is not included in recommendation engine.
# Analytics product groups mapped with learning flows and sub type flows.
ANALYTIC_PRODUCT_ID_TO_SHINE_PRODUCT_ID = {
    1: "application_highlighter",
    2: "skills_assessment",
    3: "featured_profile",
    4: "international_profile_update",
    5: "international_resume",
    6: "interview_preparation",
    7: "jobs_on_the_move",
    8: "linkedin_profile",
    9: "resume_builder",
    10: "expert_help",
    11: "shine_premium",
}

ANALYTIC_TO_LEARNING_PRODUCTFLOWS={
    1:{'type_flow':[],'sub_type_flow':[503,504]},
    2:{'type_flow':[16],'sub_type_flow':[]},
    3:{'type_flow':[5,7],'sub_type_flow':[501]},
    4:{'type_flow':[4],'sub_type_flow':[]},
    5:{'type_flow':[12],'sub_type_flow':[]},
    6:{'type_flow':[16],'sub_type_flow':[]},
    7:{'type_flow':[5],'sub_type_flow':[502]},
    8:{'type_flow':[8],'sub_type_flow':[]},
    9:{'type_flow':[17,1],'sub_type_flow':[]},
    10:{'type_flow':[],'sub_type_flow':[101]},
    11:{'type_flow':[17],'sub_type_flow':[]},
}


try:
    from .settings_local import *
except:
    pass




