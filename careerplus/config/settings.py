from .base_settings import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_LIVE = False

ALLOWED_HOSTS = ['*']
SITE_ID = 1
SITE_DOMAIN = '127.0.0.1:8000'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'careerplus1',
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

META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'learning.shine.com'
META_SITE_TYPE = 'Website'
META_SITE_NAME = 'ShineLearning'
META_USE_SITES = False
META_DEFAULT_KEYWORDS = ['E-Learning', 'Skills', 'Resume', 'India']
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
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

ROUNDONE_DEFAULT_CP_EMAIL = "careerplus@shine.com"

if DEBUG or not IS_LIVE:
    # ROUNDONE_API_BASEURL_ORDER = "http://testing.roundone.asia"
    # ROUNDONE_API_BASEURL = "http://api.roundone.asia"
    ROUNDONE_API_BASEURL = "http://api.roundone.in"  # "http://api.roundone.asia"
    ROUNDONE_API_BASEURL_ORDER = "http://www.roundone.in"  # "http://testing.roundone.asia"
    ROUNDONE_ORDER_SECRET_KEY = 'xHVEbrvpiH8BMol5rZt7YuDO'
    ROUNDONE_JOBDETAIL_SECRET_KEY = 'cQMYGVYxrMqHGPSAZeRDm4G'
    ROUNDONE_CP_CLIENT_ID = 'lnVPB3Oe9YPA3g)!F9zrFbg'
    ROUNDONE_CP_CLIENT_SECRET = 'c&OMxZ^0T*6qvyi0e3lU9OjWc!(%Wp+'
    ROUNDONE_ENCODING_KEY = 'roundonetestkey'
    ROUNDONE_ENCODING_SALT = 'roundonetestsalt'
    ROUNDONE_DEFAULT_PASSWORD = 'cp@roundone'
    ROUNDONE_API_TIMEOUT = 5
    SHINE_API_TIMEOUT = 5
else:
    ROUNDONE_API_BASEURL = "http://api.roundone.in"  # This is the live api
    ROUNDONE_API_BASEURL_ORDER = "http://www.roundone.in"
    ROUNDONE_ORDER_SECRET_KEY = 'xHVEbrvpiH8BMol5rZt7YuDO'
    ROUNDONE_JOBDETAIL_SECRET_KEY = 'cQMYGVYxrMqHGPSAZeRDm4G'
    ROUNDONE_CP_CLIENT_ID = 'lnVPB3Oe9YPA3g)!F9zrFbg'
    ROUNDONE_CP_CLIENT_SECRET = 'c&OMxZ^0T*6qvyi0e3lU9OjWc!(%Wp+'
    ROUNDONE_ENCODING_KEY = '#r0und0n3k3y'
    ROUNDONE_ENCODING_SALT = '#r0und0n354l7'
    ROUNDONE_DEFAULT_PASSWORD = 'cp@roundone'
    ROUNDONE_API_TIMEOUT = 60
    SHINE_API_TIMEOUT = 5

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

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]
CITIES_LIGHT_APP_NAME = 'geolocation'

# Shine settings
SHINE_SITE = 'https://sumosc1.shine.com'
CLIENT_ACCESS_KEY = "M2XFaFVHHJwlISEQxFQis1cQoKe6lIBKUGaEDG0WiHA"
CLIENT_ACCESS_SECRET = "aSQrGC9VZ866os5AZNGsor4CThxfGNz3s8V7rSMX3TY"
SHINE_API_USER = 'scpapiuser@gmail.com'
SHINE_API_USER_PWD = 'tarun@123'
SHINE_API_TIMEOUT = 60


# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #  email backend as console.
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'upendra.rockon@gmail.com'
# EMAIL_HOST_PASSWORD = '9616744875'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# VARIABLE FOR SENDING RESUME SERVICES MAILS
CANDIDATES_EMAIL = 'Shine.com <candidates@shine.com>'
CONSULTANTS_EMAIL = 'Shine.com <careerplus@shine.com>'
REPLY_TO = 'resume@shine.com'

EMAIL_HOST = '172.22.65.55'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = 0
SERVER_EMAIL = 'recruiter@shine.com'
DEFAULT_FROM_EMAIL = CONSULTANTS_EMAIL
EMAIL_SERVER = 'http://localhost:8000'

# encode decode settings
EMAIL_SMS_TOKEN_EXPIRY = 7
ENCODE_SALT = 'xfxa'


# Do Not Change #
COURSE_SLUG = ['course',]
WRITING_SLUG = ['writing',]
SERVICE_SLUG = ['service',]


VENDOR_GROUP_LIST = ['VENDOR']
PRODUCT_GROUP_LIST = ['PRODUCT']
OPERATION_GROUP_LIST = ['OPERATION', 'OPS_HEAD']
SEO_GROUP_LIST = ['SEO']
WRITING_GROUP_LIST = ['WRITERS']

# Booster Recruiters
BOOSTER_RECRUITERS = ['akamarnath2@gmail.com']

CP_VENDOR_ID = '12345'

############ SOLR SETTINGS #######################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}
