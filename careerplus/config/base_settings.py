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
sys.path.append(os.path.join(BASE_DIR, 'apps'))


GEOIP_PATH = BASE_DIR + '/apps/users/GeoIP.dat'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g58#1(xdr&s%t@$erwjosc@nuiuy4j)9#g+*jhr#m1o6c)zws7'


TEMPLATE_DEBUG = False  # django sorl required


# Application definition
DJANGO_APPS = [
    'grappelli',
    'filebrowser',
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
    'rest_framework',
    'haystack',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'core',
    'users',
    'cms',
    'design',
    'faq',
    'seo',
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
    'blog',
    'homepage',
    'microsite',
    'search',
    'linkedin',
    'emailers',
    'quizs',
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
                'django_mobile.context_processors.flavour',
                'careerplus.config.context_processors.common_context_processor',
                'sekizai.context_processors.sekizai',
                'core.context_processors.js_settings'
            ],
            'loaders': [
                # ('django_mobile.loader.CachedLoader', [
                    'django_mobile.loader.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                # ]),
            ],
        },
    },
]

# For django-mobile compatiility
TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']

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
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser'
    ],
    'PAGE_SIZE': 10
}

CKEDITOR_UPLOAD_PATH = "uploads/ck_editor/"
CKEDITOR_JQUERY_URL = 'shinelearn/js/common/jquery.min.js'  #'https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': 700,
        # 'removePlugins': 'stylesheetparser',
        # 'extraPlugins': 'codesnippet',
    },
}


# BROKER_URL = 'redis://localhost:6379/0'

# try:
#     REDIS_CON = redis.StrictRedis(host='localhost', port=6379, db=0)
# except:
#     REDIS_CON = None

DRAFT_MAX_LIMIT = 3

# HTMSL for SMS
HTMSL_USER = 'sumo'
HTMSL_PASS = 'w1XN75L'
HTMSL_URL = 'http://172.22.65.226/smspush-enterprise/api/push'
ACCESSKEY = 'PCQwpGAFOHh3KxUj89nKYc4TtSKq9V'


########## DOMAIN SETTINGS ######################
MAIN_DOMAIN_PREFIX = 'http://learning.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)

############ SOLR SETTINGS #######################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'INCLUDE_SPELLING': False,
    },
}

HAYSTACK_ITERATOR_LOAD_PER_QUERY = 100
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50
HAYSTACK_BATCH_SIZE = 100
HAYSTACK_LIMIT_TO_REGISTERED_MODELS = False

# encode decode constants
TOKEN_DT_FORMAT = '%Y%m%d%H%M%S'
LOGIN_TOKEN_EXPIRY = 30
EMAIL_SMS_TOKEN_EXPIRY = 7
ENCODE_SALT = 'xfxa'

# resume writing India product List
RESUME_WRITING_INDIA = [2]
