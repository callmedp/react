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
SECRET_KEY = 'g58#1(xdr&s%t@$erwjosc@nuiuy4j)9#g+*jhr#m1o6c)zws7'

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
    'compressor'
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
    'talenteconomy'
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
    'core.middleware.TrackingMiddleware'
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
    'compressor.filters.cssmin.rCSSMinFilter',
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
        'rest_framework.permissions.IsAdminUser'
    ],
    'PAGE_SIZE': 10,
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


BROKER_URL = 'redis://localhost:6379/0'

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

CART_MAX_LIMIT = 5

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
LOGS_ROOT = os.path.join(BASE_DIR, "log")

for d in ['debug', 'error', 'info', 'email', 'sms', 'profile', 'payment']:
    if not os.path.exists(os.path.join(LOGS_ROOT, d)):
        os.makedirs(os.path.join(LOGS_ROOT, d))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(lineno)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'debug', 'debug.log')
        },
        'info_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'info', 'info.log')
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'error', 'error.log')
        },
        'email_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'email', 'email.log')
        },
        'sms_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'sms', 'sms.log')
        },
        'profile_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'profile', 'profile.log')
        },
        'unsubs_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'info', 'unsubs.log')
        },
        'feedback_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'email', 'feedback.log')
        },
        'payment_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'payment', 'error.log')
        },
        'cron_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'error', 'cron.log')
        },
        'command_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'error', 'command.log')
        },
        'cashback_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_ROOT, 'error', 'cashback.log')
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'error_handler'],
            'level': 'ERROR',
            'propagate': True,
        },
        'debug_log': {
            'handlers': ['debug_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'info_log': {
            'handlers': ['info_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'error_log': {
            'handlers': ['error_handler'],
            'level': 'ERROR',
            'propagate': True,
        },
        'email_log': {
            'handlers': ['email_handler', ],
            'level': 'INFO',
            'propagate': True,
        },
        'sms_log': {
            'handlers': ['sms_handler', ],
            'level': 'INFO',
            'propagate': True,
        },
        'profile_import_log': {
            'handlers': ['profile_handler', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'unsubs_log': {
            'handlers': ['unsubs_handler', ],
            'level': 'INFO',
            'propagate': True,
        },
        'feedback_log': {
            'handlers': ['feedback_handler', ],
            'level': 'INFO',
            'propagate': True,
        },
        'payment_log': {
            'handlers': ['payment_handler', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'cron_log': {
            'handlers': ['cron_handler', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'command_log': {
            'handlers': ['command_handler', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'cashback_log': {
            'handlers': ['cashback_handler', ],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


############ SEARCH SPECIFIC SETTINGS ##############
PRODUCT_ALTERNATE_SEARCH_TERMS = []     # TODO: Enter commonly search terms


###### CLICK TRACKING #######################
CLICK_TRACKING = 'https://www3.shine.com/click-tracking/'


####### PRODUCT SETTINGS ####################
# Do Not Change #
COURSE_SLUG = ['course', ]
WRITING_SLUG = ['writing', 'resume']
SERVICE_SLUG = ['service', ]
DELIVERY_SLUG = ['normal', 'express', 'super-express']
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
WRITING_GROUP_LIST = ['Writer', 'WRITER HEADS']
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