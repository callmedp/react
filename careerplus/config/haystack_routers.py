#python imports

#django imports

#local imports

#inter app imports

#third party imports
from haystack.routers import BaseRouter
from haystack.constants import DEFAULT_ALIAS


class MasterSlaveRouter(BaseRouter):
    
    def for_read(self, **hints):
        return DEFAULT_ALIAS

    def for_write(self, **hints):
        return "index"