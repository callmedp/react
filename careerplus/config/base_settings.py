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


GEOIP_PATH = BASE_DIR + '/apps/users/GeoIP.dat'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
###### KEYS ################################
SECRET_KEY = 'g58#1(xdr&s%t@$erwjosc@nuiuy4j)9#g+*jhr#m1o6c)zws7'
MOBILE_ADSERVER_ENCODE_KEY = 'el!bomen!h$'
ACROSS_ENCODE_KEY = '@$h1n3c4r33rplu5'

TEMPLATE_DEBUG = False  # django sorl required


# Application definition
DJANGO_APPS = [
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
    'storages'
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
    'scheduler',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.UpgradedMobileDetectionMiddleware',
    'core.middleware.UpgradedSetFlavourMiddleware',
    'core.middleware.LearningShineMiddleware',
    'core.middleware.LoginMiddleware',
    'core.middleware.TrackingMiddleware',
    'core.middleware.AmpMiddleware',
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
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.common_context_processor',
                'django_mobile.context_processors.flavour',
                'sekizai.context_processors.sekizai',
                'core.context_processors.js_settings'
            ],
            'loaders': ([
                # ('django_mobile.loader.CachedLoader', [
                    'django_mobile.loader.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                ]),
        },
    },
]

# For django-mobile compatiility
TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']
DEFAULT_MOBILE_FLAVOUR = 'mobile'
FLAVOURS = ('full', 'mobile')

WSGI_APPLICATION = 'careerplus.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
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

LEAD_UPLOAD = os.path.join(BASE_DIR, 'media/uploads/lead_file/')

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')
STATIC_URL = '/media/static/'

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
    'PAGE_SIZE': 100,
}

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 10,
    'OAUTH_DELETE_EXPIRED': True,
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

# ckeditor settings...
CKEDITOR_UPLOAD_PATH = "uploads/ck_editor/"
CKEDITOR_JQUERY_URL = 'shinelearn/js/common/jquery.min.js'  #'https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 'auto',
        'width': 'auto',
        # 'removePlugins': 'stylesheetparser',
        # 'extraPlugins': 'codesnippet',
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
SITE_DOMAIN = 'learning.shine.com'
SITE_PROTOCOL = 'https'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN) #'http://learning.shine.com'
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
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]
CITIES_LIGHT_APP_NAME = 'geolocation'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_core')]
# encode decode constants
TOKEN_DT_FORMAT = '%Y%m%d%H%M%S'
LOGIN_TOKEN_EXPIRY = 15
EMAIL_SMS_TOKEN_EXPIRY = 7
ENCODE_SALT = 'xfxa'

# Url Shortner
URL_SHORTENER_API = 'https://www.googleapis.com/urlshortener/v1/url'
URL_SHORTENER_ACCESS_KEY='AIzaSyBtmK_SIBfhb_hXkgLlfk7IwVlnKZxTb2I'

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
        '':{
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


PRODUCT_ALTERNATE_SEARCH_TERMS = []     # TODO: Enter commonly search terms


###### CLICK TRACKING #######################
CLICK_TRACKING = 'https://www3.shine.com/click-tracking/'


####### PRODUCT SETTINGS ####################
# Do Not Change #
COURSE_SLUG = ['course', ]
WRITING_SLUG = ['writing', 'resume']
SERVICE_SLUG = ['service', ]
# delivery slug
NORMAL_DELIVERY_SLUG = ['normal', ]
EXPRESS_DELIVERY_SLUG = ['express', ]
SUPER_EXPRESS_DELIVERY_SLUG = ['super-express', ]
DELIVERY_SLUG = NORMAL_DELIVERY_SLUG + EXPRESS_DELIVERY_SLUG + SUPER_EXPRESS_DELIVERY_SLUG

CHARS_TO_REMOVE = ['/', "'", "(", ")", "!", "~", "`", "@", "#", "$", "%", "&" ]
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

#BLOGGER#
LEARNING_BLOGGER = ['LEARNING_BLOGGER']
TALENT_BLOGGER = ['TALENT_BLOGGER']
BLOGGER_GROUP_LIST = [LEARNING_BLOGGER, TALENT_BLOGGER, PRODUCT_GROUP_LIST]
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
USER_QUERY_GROUP_LIST = CMS_GROUP_LIST + SKILL_GROUP_LIST + COURSE_GROUP_LIST + SERVICE_GROUP_LIST

# Marketing User Auto login token Generation
MARKETING_GROUP_LIST = ['MARKETING']


# Course catalogoue cache time
COURSE_CATALOGUE_CASH_TIME = 24 * 60 * 60  # in seconds

####### EMAIL SETTINGS #########
ROUNDONE_DEFAULT_CP_EMAIL = "learning@shine.com"
CONSULTANTS_EMAIL = 'Shine.com <learning@shine.com>'
REPLY_TO = 'resume@shine.com'

##### CCAVENUE SETTINGS ############
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'
SESSION_CACHE_ALIAS = 'session'
SESSION_ENGINE = "django.contrib.sessions.backends.cache"


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PROJECT_DIR + '/careerplus/config/code-learning-key.json'
