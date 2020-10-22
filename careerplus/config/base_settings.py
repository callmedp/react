"""
Django settings for careerplus project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

# import redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(os.path.join(BASE_DIR, 'apps'))

GEOIP_PATH = BASE_DIR + '/apps/users/GeoLite2.mmdb'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
###### KEYS ################################
SECRET_KEY = 'g58#1(xdr&s%t@$erwjosc@nuiuy4j)9#g+*jhr#m1o6c)zws7'
MOBILE_ADSERVER_ENCODE_KEY = 'el!bomen!h$'
ACROSS_ENCODE_KEY = '@$h1n3c4r33rplu5'

TEMPLATE_DEBUG = False  # django sorl required
TEST_EMAIL = True

# Application definition
DJANGO_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'cities_light',
    'ckeditor',
    'ckeditor_uploader',
    'django_mobile',
    'meta',
    'requests',
    'sekizai',
    'sorl.thumbnail',
    'oauth2_provider',
    'rest_framework',
    'haystack',
    'celery',
    'compressor',
    'storages',
    'django_filters',
    'webpack_loader',
    'corsheaders' ,
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'core',
    'users',
    'seo',
    'blog',
    'cms',
    'design',
    'faq',
    'ajax',
    'skillpage',
    'review',
    'geolocation',
    'console',
    'coupon',
    'partner',
    'payment',
    'shop',
    'cart',
    'order',
    'homepage',
    'microsite',
    'dashboard',
    'wallet',
    'search',
    'linkedin',
    'emailers',
    'quizs',
    'crmapi',
    'api',
    'marketing',
    'talenteconomy',
    'hrinsider',
    'scheduler',
    'resumebuilder',
    'assessment',
    'resumescorechecker',
    'tinymce',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.RemoveSessionCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'core.middleware.UpgradedMobileDetectionMiddleware',
    'core.middleware.UpgradedSetFlavourMiddleware',
    'core.middleware.LearningShineMiddleware',
    'core.middleware.LoginMiddleware',
    'core.middleware.TrackingMiddleware',
    'core.middleware.AmpMiddleware',
    'core.middleware.LocalIPDetectionMiddleware',
]

ROOT_URLCONF = 'careerplus.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.common_context_processor',
                'django_mobile.context_processors.flavour',
                'sekizai.context_processors.sekizai',
                'core.context_processors.js_settings',
                'core.context_processors.marketing_context_processor',
                'core.context_processors.getSearchSet',
                'core.context_processors.get_console_sidebar_badges'
            ],
            'loaders': ([
                # ('django_mobile.loader.CachedLoader', [
                'django_mobile.loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        },
    },
]

# For django-mobile compatiility
TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']
DEFAULT_MOBILE_FLAVOUR = 'mobile'
FLAVOURS = ('full', 'mobile')

WSGI_APPLICATION = 'careerplus.wsgi.application'

# Webpack loader is used to load webpack generated files
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'react/dist/desktop/',
        'STATS_FILE': os.path.join(BASE_DIR, '..', 'webpack-desktop-stats.json'),
    },
    'MOBILE': {
        'BUNDLE_DIR_NAME': 'react/dist/mobile/',
        'STATS_FILE': os.path.join(BASE_DIR, '..', 'webpack-mobile-stats.json'),
    },
    'SCORE-CHECKER-DESKTOP': {
        'BUNDLE_DIR_NAME': 'score-checker/dist/desktop/',
        'STATS_FILE': os.path.join(BASE_DIR, '..', 'webpack-score-checker-desktop-stats.json'),
    },
    'SCORE-CHECKER-MOBILE': {
        'BUNDLE_DIR_NAME': 'score-checker/dist/mobile/',
        'STATS_FILE': os.path.join(BASE_DIR, '..', 'webpack-score-checker-mobile-stats.json'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10, }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'careerplus.config.admin_validator.NumberValidator'
    },
    {
        'NAME': 'careerplus.config.admin_validator.UppercaseValidator'
    },
     {
        'NAME': 'careerplus.config.admin_validator.LowercaseValidator'
    },
    {
        'NAME': 'careerplus.config.admin_validator.PunctuationValidator'
    },
    
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
)

COMPRESS_PRECOMPILERS = (
    ('text/scss', 'sass --scss {infile} {outfile}'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
GCP_MEDIA_LOCATION = "l/m/"

LEAD_UPLOAD = os.path.join(BASE_DIR, 'media/uploads/lead_file/')

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')
STATIC_URL = '/media/static/'
GCP_STATIC_LOCATION = "l/s/"

DOWNLOAD_ROOT = os.path.join(BASE_DIR, 'download')
DOWNLOAD_URL = '/download/'

INVOICE_DIR = os.path.join(BASE_DIR, 'media/invoice/')
RESUME_DIR = os.path.join(BASE_DIR, 'media/resume/')

REST_FRAMEWORK = {
    # authentication permission
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 24,
    'OAUTH_DELETE_EXPIRED': True,
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

# ckeditor settings...
CKEDITOR_UPLOAD_PATH = "uploads/ck_editor/"
CKEDITOR_JQUERY_URL = 'shinelearn/js/common/jquery.min.js'  # 'https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 'auto',
        'width': 'auto',
        # 'removePlugins': 'stylesheetparser',
        # 'extraPlugins': 'codesnippet',
        # 'extraAllowedContent': 'iframe[*]',
    },
}
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_REQUIRE_STAFF = False

######## CELERY SETTINGS ###########
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = (
    'emailers.tasks',
)

# try:
#     REDIS_CON = redis.StrictRedis(host='localhost', port=6379, db=0)
# except:
#     REDIS_CON = None

DRAFT_MAX_LIMIT = 3

# GST tax rate on product
TAX_RATE_PERCENTAGE = 18

# HTMSL for SMS
HTMSL_USER = 'sumo'
HTMSL_PASS = 'Firefly@456'
HTMSL_URL = 'https://alerts.solutionsinfini.com/api/v4/'
ACCESSKEY = 'Af7fa4f7dacdc996393c18071b57d0a6f'

########## DOMAIN SETTINGS ######################
SITE_DOMAIN = 'http://127.0.0.1:8000/'
MOBILE_SITE_DOMAIN = 'mlearning.shine.com'
SITE_PROTOCOL = 'https'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)  # 'http://learning.shine.com'
MOBILE_PROTOCOL_DOMAIN = '{}://{}'.format(SITE_PROTOCOL,SITE_DOMAIN)
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)
SITE_ID = 1
CART_MAX_LIMIT = 5
META_SITE_TYPE = 'Website'
META_SITE_NAME = 'ShineLearning'
META_USE_SITES = True
META_DEFAULT_KEYWORDS = ['E-Learning', 'Skills', 'Resume', 'India']
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = False
META_USE_GOOGLEPLUS_PROPERTIES = True
META_FB_TYPE = 'Website'
META_GPLUS_TYPE = 'Website'

############ SOLR SETTINGS #######################
HAYSTACK_ITERATOR_LOAD_PER_QUERY = 100
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
HAYSTACK_BATCH_SIZE = 100
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False
##################################################

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR',
                                   'PPLS', 'STLMT', ]
CITIES_LIGHT_APP_NAME = 'geolocation'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_core')]
# encode decode constants
TOKEN_DT_FORMAT = '%Y%m%d%H%M%S'
LOGIN_TOKEN_EXPIRY = 15
EMAIL_SMS_TOKEN_EXPIRY = 7
ENCODE_SALT = 'xfxa'

# Url Shortner
URL_SHORTENER_API = 'https://www.googleapis.com/urlshortener/v1/url'
URL_SHORTENER_ACCESS_KEY = 'AIzaSyBtmK_SIBfhb_hXkgLlfk7IwVlnKZxTb2I'

# resume writing India product List
RESUME_WRITING_INDIA = [2]

######## LOGGING CONFIG ############################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': 'shinelearning_%(name)s: %(levelname)s %(asctime)s %(pathname)s %(lineno)s %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local4',
            'formatter': 'simple'
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local4',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # root logger
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'INFO',
            'disabled': False
        },
        'django.request': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
        'info_log': {
            'handlers': ['syslog'],
            'level': 'INFO',
            'propagate': True,
        },
        'error_log': {
            'handlers': ['syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

PRODUCT_ALTERNATE_SEARCH_TERMS = []  # TODO: Enter commonly search terms

###### CLICK TRACKING #######################
CLICK_TRACKING = 'https://www3.shine.com/click-tracking/'

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOW_CREDENTIALS = False

CORS_ORIGIN_WHITELIST = ('*',)
#
# CORS_ALLOW_METHODS = (
#     'DELETE',
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
# )

####### PRODUCT SETTINGS ####################
# Do Not Change #
COURSE_SLUG = ['course', ]
WRITING_SLUG = ['writing', 'resume']
SERVICE_SLUG = ['service', ]
ASSESSMENT_SLUG = ['assessment']
# delivery slug
NORMAL_DELIVERY_SLUG = ['normal', ]
EXPRESS_DELIVERY_SLUG = ['express', ]
SUPER_EXPRESS_DELIVERY_SLUG = ['super-express', ]
DELIVERY_SLUG = NORMAL_DELIVERY_SLUG + EXPRESS_DELIVERY_SLUG + SUPER_EXPRESS_DELIVERY_SLUG

CHARS_TO_REMOVE = ['/', "'", "(", ")", "!", "~", "`", "@", "#", "$", "%", "&"]
############################################

# google captcha settings
GOOGLE_RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"
GOOGLE_RECAPTCHA_KEY = '6Lfa5zYUAAAAAFFe_gV2u2h3XovQzmQCUzRm4MYY'
GOOGLE_RECAPTCHA_SECRET = '6Lfa5zYUAAAAAAke3_HJ7XgC3Voxbdn1bscy878R'

###### SSL Settings ##########
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# group list
VENDOR_GROUP_LIST = ['VENDOR', 'STUDY_MATE']
PRODUCT_GROUP_LIST = ['PRODUCT']
OPERATION_GROUP_LIST = ['OPERATION', 'OPS_HEAD']
SEO_GROUP_LIST = ['SEO']
WRITING_GROUP_LIST = ['WRITER', 'WRITER_HEAD']
BLOG_WRITER_GROUP_LIST = ['BLOG_WRITER']

# BLOGGER#
LEARNING_BLOGGER = ['LEARNING_BLOGGER']
TALENT_BLOGGER = ['TALENT_BLOGGER']
HR_INSIDER = ['HR_INSIDER']
BLOGGER_GROUP_LIST = [LEARNING_BLOGGER, TALENT_BLOGGER, HR_INSIDER, PRODUCT_GROUP_LIST]

# Refund Application level
OPS_GROUP_LIST = ['OPERATION']
OPS_HEAD_GROUP_LIST = ['OPS_HEAD']
BUSINESS_HEAD_GROUP_LIST = ['BUSINESS_HEAD']
DEPARTMENT_HEAD_GROUP_LIST = ['DEPARTMENT_HEAD']
FINANCE_GROUP_LIST = ['FINANCE']
BUSINESS_APPROVAL_LIMIT = 25000  # refund
REFUND_GROUP_LIST = OPS_GROUP_LIST + OPS_HEAD_GROUP_LIST + BUSINESS_HEAD_GROUP_LIST + DEPARTMENT_HEAD_GROUP_LIST + FINANCE_GROUP_LIST

# User Query Group
CMS_GROUP_LIST = ['CMS_USER']
SKILL_GROUP_LIST = ['SKILL_USER']
COURSE_GROUP_LIST = ['COURSE_USER']
SERVICE_GROUP_LIST = ['SERVICE_USER']
ASSIGNMENT_GROUP_LIST = ['ASSIGNMENT_USER']
USER_QUERY_GROUP_LIST = CMS_GROUP_LIST + SKILL_GROUP_LIST + COURSE_GROUP_LIST + SERVICE_GROUP_LIST + ASSIGNMENT_GROUP_LIST

# Marketing User Auto login token Generation
MARKETING_GROUP_LIST = ['MARKETING']

# welcome call Group List
WELCOMECALL_GROUP_LIST = ['WELCOME_CALL']

REFUND_GROUP_LIST += WELCOMECALL_GROUP_LIST

# Course catalogoue cache time
COURSE_CATALOGUE_CASH_TIME = 24 * 60 * 60  # in seconds

####### EMAIL SETTINGS #########
ROUNDONE_DEFAULT_CP_EMAIL = "learning@shine.com"
CONSULTANTS_EMAIL = 'Shine.com <learning@shine.com>'
REPLY_TO = 'resume@shine.com'
TAG_MAILER = False

##### CCAVENUE SETTINGS ############
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'
SESSION_CACHE_ALIAS = 'session'
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PROJECT_DIR + '/careerplus/config/code-learning-key.json'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 year
CONSOLE_SESSION_TIMEOUT = 60 * 60 * 24

CMS_STATIC_TEMP_DICT = {
    1: 'cms_static.html',
    3: 'static_resignation_page.html',
    7: 'static_cover_page.html'}

IS_MAINTENANCE = False
MAINTENANCE_MESSAGE = "This site will be under maintenance from 9 pm to 12 pm on Friday, 11th Jan, 2019."

############ MARKETING PAGES MAPPING WITH ID

URL_MAPPING_TO_PRODUCT = {"resume-writing-services-1": ([1921, 1922, 1923, 1924, 32], 1921)
    , "linkedin-1": ([1926, 1925, 1927, 1928, 33], 1926),
                          "aws-cert": ([3133], 3133),
                          "ban-cert": ([3133], 3133),
                          "data-scientist": ([3417], 3417),
                          "ifrs-cert": ([1880], 1880),
                          "gst-certification": ([1810], 1810),
                          "data-science": ([3417], 3417),
                          "six-sigma": ([3400], 3400),
                          "linkedin": ([1926], 1926),
                          'devops-professional': ([4131],4131),

                          }

LOCAL_NETWORK_IPS_RANGE = ["59.160.104.0/24", "220.227.160.128/25", "122.177.0.0/16", "172.22.65.0/24",
                           "125.23.128.20/30", "59.144.72.128/28", "203.145.175.0/28", "103.248.118.192/28"]

LOCAL_NETWORK_IPS = ["172.16.64.80", "125.19.44.195", "124.124.86.138", "115.112.32.194", "115.254.3.5",
                     "59.160.104.254", "59.160.104.5", "103.245.33.42", "172.16.64.105", "111.93.231.2",
                     "122.160.111.100", "59.160.104.254", "59.160.104.248", "122.15.40.51", "125.19.44.195",
                     "122.15.29.195", "59.160.104.150", "122.15.44.233", "103.248.118.194", "106.215.170.236",
                     "182.64.252.176", "125.17.83.97", "220.225.255.161", "118.102.181.219", "220.227.36.202",
                     "202.164.38.195", "122.162.129.43", "192.168.1.5", "223.179.134.80", "223.179.151.72",
                     "122.162.42.142", "171.79.76.124"]

MEDIA_ALLOWED_CONTENT_TYPES = ['image/jpeg', 'image/jpg', 'image/gif', 'image/png', 'image/svg', 'image/svg+xml', \
                               'video/x-flv', 'video/mp4', 'application/x-mpegURL', 'video/MP2T', 'video/3gpp', \
                               'video/quicktime', ' video/x-msvideo', 'video/x-ms-wmv', 'video/webm', 'application/pdf', \
                               'application/msword',
                               'application/vnd.openxmlformats-officedocument.wordprocessingml.document', \
                               'application/vnd.ms-excel',
                               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', \
                               'application/vnd.ms-powerpoint',
                               'application/vnd.openxmlformats-officedocument.presentationml.presentation']


RESUME_TEMPLATE_DIR = "resume-builder"

#Haystack Settings
HAYSTACK_ROUTERS = ['careerplus.config.haystack_routers.MasterSlaveRouter', 'haystack.routers.DefaultRouter']

#JOTM Default Message
WHATS_APP_MESSAGE_FORMAT = '''Here are our job recommendations for this week.<br>
                        <br>{}Please do not call/reply directly to this message<br><br>In case of any queries, you can call us on  08047105151 or email us at resume@shine.com<br><br>Thanks,<br><br>Team Shine
                        '''
#Candidate Mongo Settings
CANDIDATE_MONGO_PORT = ':27017'
CANDIDATE_MONGO_USERNAME = 'candadmin'
CANDIDATE_MONGO_PASSWORD = 'candadmin'
CANDIDATE_MONGO_INSTANCE_STR = '172.22.67.226:27017'
CANDIDATE_MONGO_DB = 'sumoplus'

MAIL_COUNTDOWN = 900
PRODUCT_LEADCREATION_COUNTDOWN = 300

TEST_PREP_ID = [556]
TEST_PREP_CHILDREN_ID = [564,529,558,561,562,559,560,563]

#Candidate Mongo Settings
CANDIDATE_MONGO_PORT = ':27017'
CANDIDATE_MONGO_USERNAME = 'candadmin'
CANDIDATE_MONGO_PASSWORD = 'candadmin'
CANDIDATE_MONGO_INSTANCE_STR = '172.22.67.226:27017'
CANDIDATE_MONGO_DB = 'sumoplus'


ZESTMONEY_INFO = {
                "authentication_base_url":"https://staging-auth.zestmoney.in",
                "api_base_url":"https://staging-app.zestmoney.in",
                "user_name":"ShineLearning",
                "password":"IWo)2IDs",
                "client_id":"e32b336c-74ab-4254-82a6-3d9ebd9242d0",
                "client_secret":"Zaoz?KPq%}=7=CTYdbVs"
                }
PAYU_INFO = {'merchant_salt':'JN7rUoRe',
            'merchant_key':'ng7s88',
            'payment_url':'https://test.payu.in/_payment',
            'web_api_url':'https://test.payu.in/merchant/postservice.php?form=2'}


PAYU_INFO1 = {'merchant_salt': 'DiRp9kCs',
             'merchant_key': 'XzRABA',
             'payment_url': 'https://test.payu.in/_payment',
             'web_api_url': 'https://test.payu.in/merchant/postservice.php?form=2', }


# Redirect obsolete article to category page.
REDIRECT_ARTICLE = {
    1: '/talenteconomy/career-help/',
    15: '/talenteconomy/career-help/'
}
REDIRECT_ARTICLE_CATEGORY = [
    'job-search-guidance',
    'competitive-exams'
]
REDIRECT_ARTICLE_CATEGORY_TE_CATEGORY = {
    'competitive-exams': '/talenteconomy/career-help/'
}


# default recommend products to be shown
DEFAULT_RECOMMEND_PRODUCT = [2634, 2787,1,4]


RESUME_SHINE_SITE_PROTOCOL = 'https'
RESUME_SHINE_SITE_DOMAIN = 'resume.shine.com'
RESUME_SHINE_MAIN_DOMAIN = '{}://{}'.format(RESUME_SHINE_SITE_PROTOCOL,RESUME_SHINE_SITE_DOMAIN)


PAYU_POST_URL = "https://test.payu.in/_payment"


PAYU_INFO1 = {'merchant_salt': 'DiRp9kCs',
             'merchant_key': 'XzRABA',
             'payment_url': 'https://test.payu.in/_payment',
             'web_api_url': 'https://test.payu.in/merchant/postservice.php?form=2', }



RSHINE_CCAVENUE_ACCESS_CODE = 'AVNZ03HE25BR73ZNRB'
RSHINE_CCAVENUE_WORKING_KEY = 'FBD9C0D0B8D397CD4E182B9BFF6EA44F'

'''
links for analytics vidhya 
'''
ANALYTICS_VIDHYA_URL = {
    'BASE_URL' : 'https://id.analyticsvidhya.com',
    'USERNAME' : 'rajila.madhavan@hindustantimes.com',
    'PASSWORD' : 'shine123',
    'ENROLLMENT' : '/api/enrollments/requests',
    'STATUS' : '/api/enrollments/requests/{}'
}
'''
link end
'''
THUMBNAIL_PRESERVE_FORMAT = True


RAZOR_PAY_DICT = {
    'key_id': 'rzp_test_Oca8UTneyg6bwO',
    'key_secret': 'km5KILWfr6sF7XzaDoC5kGOj',
}



