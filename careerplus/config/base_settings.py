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
import redis

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
    'ckeditor',
    'ckeditor_uploader',
    'meta',
    'cities_light',
    'sorl.thumbnail',
    'requests'
]

# Apps specific for this project go here.
LOCAL_APPS = [
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
    'microsite',
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
]

ROOT_URLCONF = 'careerplus.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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


BROKER_URL = 'redis://localhost:6379/0'

try:
    REDIS_CON = redis.StrictRedis(host='localhost', port=6379, db=0)
except:
    REDIS_CON = None

CART_MAX_LIMIT = 5
