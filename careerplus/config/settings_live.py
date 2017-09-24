from .settings import *

DEBUG = False
IS_LIVE = True

########## DOMAIN SETTINGS ######################
MAIN_DOMAIN_PREFIX = 'http://learning1.shine.com'
SITE_DOMAIN = 'learning1.shine.com'
SITE_PROTOCOL = 'http'
SHINE_SITE = 'https://shine.com'
SHINE_API_URL = 'https://shine.com/api/v2'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}