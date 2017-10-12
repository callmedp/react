from .settings import *


########## DOMAIN SETTINGS ######################
SITE_DOMAIN = 'learning1.shine.com'
SITE_PROTOCOL = 'https'
MAIN_DOMAIN_PREFIX = '{}://{}'.format(SITE_PROTOCOL, SITE_DOMAIN)  #'http://learning.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}

SHINE_SITE = 'https://sumosc.shine.com'
SHINE_API_URL = 'https://sumosc.shine.com/api/v2'

CELERY_ALWAYS_EAGER = False


####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC49XECC'
CCAVENUE_WORKING_KEY = 'DE002F3C615C11E7FB7D333050103230'
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'
DEBUG = True
IS_LIVE = False

from .settings_local import *