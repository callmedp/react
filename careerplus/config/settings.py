from .base_settings import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerplus',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    },
}

# Apps specific for this project go here.
DEV_APPS = [
    'debug_toolbar'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + DEV_APPS

DEV_MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_core')]

WSGI_APPLICATION = 'careerplus.config.wsgi.application'

INTERNAL_IPS = ('127.0.0.1',)
