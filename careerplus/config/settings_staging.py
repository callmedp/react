from .settings import *


########## DOMAIN SETTINGS ######################
MAIN_DOMAIN_PREFIX = 'http://learning1.shine.com'
MOBILE_LOGIN_URL = '{}/login/'.format(MAIN_DOMAIN_PREFIX)

SITE_DOMAIN = 'learning1.shine.com'
SITE_PROTOCOL = 'http'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}