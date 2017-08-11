from .settings import *


########## DOMAIN SETTINGS ######################
MAIN_DOMAIN_PREFIX = 'http://learning1.shine.com'
SITE_DOMAIN = 'learning1.shine.com'

############ SOLR SETTINGS #######################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://172.22.65.33:8983/solr',
        'INCLUDE_SPELLING': False,
    },
}


