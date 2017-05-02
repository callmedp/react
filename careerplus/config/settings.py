from .base_settings import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
SITE_ID = 1
SITE_DOMAIN = '127.0.0.1:8000'

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

LEAD_UPLOAD = os.path.join(BASE_DIR, 'media/uploads/lead_file/')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

DOWNLOAD_ROOT = os.path.join(BASE_DIR, 'download')
DOWNLOAD_URL = '/download/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_core')]

WSGI_APPLICATION = 'careerplus.config.wsgi.application'

INTERNAL_IPS = ('127.0.0.1',)

HOST_NAME = 'http://127.0.0.1:8000'

META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'learning.shine.com'
META_SITE_TYPE = 'Website'
META_SITE_NAME = 'ShineLearning'
META_USE_SITES = False
META_DEFAULT_KEYWORDS = ['E-Learning', 'Skills', 'Resume', 'India']
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
META_SITE_TYPE = 'Website'
META_FB_TYPE = 'Website'
META_FB_APPID = '111111111111111111'
META_FB_PROFILE_ID = '11111111111111'
META_FB_PUBLISHER = 'https://facebook.com/foo.blag'
META_FB_AUTHOR_URL = 'https://facebook.com/foo.blag'
META_TWITTER_TYPE = 'summary_large_image'
META_TWITTER_SITE = '@FooBlag'
META_TWITTER_AUTHOR = '@FooBlag'
META_GPLUS_TYPE = 'Website'
META_GPLUS_AUTHOR = '+FooBar'


CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]
CITIES_LIGHT_APP_NAME = 'geolocation'
