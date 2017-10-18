from .settings import *

DEBUG = False
IS_LIVE = True
STATIC_URL = 'https://origin-static3.shine.com/'
########## DOMAIN SETTINGS ######################
MAIN_DOMAIN_PREFIX = 'http://learning1.shine.com'
SITE_DOMAIN = 'learning1.shine.com'
SITE_PROTOCOL = 'http'
SHINE_SITE = 'https://www.shine.com'
SHINE_API_URL = 'https://shine.com/api/v2'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'core.library.haystack.custom_solr_backend.CustomSolrEngine',
        'URL': 'http://172.22.65.33:8983/solr/prdt',
        'INCLUDE_SPELLING': False,
    },
}

####### CCAVENUE SETTINGS ###########################
CCAVENUE_ACCESS_CODE = 'AVEX73EI34CC49XECC'
CCAVENUE_WORKING_KEY = 'BB84397177B2D640744BA272627C2A61'
CCAVENUE_URL = 'https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction'