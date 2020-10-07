#python imports
import sys
from importlib import import_module

#django imports

#local imports
from .utils import create_request_cls,default

#inter app imports

#third party imports
# from celery.worker.request import create_request_cls as crcls

def patch_create_request_class():
    """
    Monkey Patching create_request_class function.
    Logging of task completion added.
    """
    celery_request_module = import_module("celery.worker.request")
    celery_request_module.create_request_cls = create_request_cls
    sys.modules["celery.worker.request"] = celery_request_module

def patch_default():
    """
    Monkey Patching create_request_class function.
    Logging of task completion added.
    """
    celery_strategy_module = import_module("celery.worker.strategy")
    celery_strategy_module.default = default
    sys.modules["celery.worker.strategy"] = celery_strategy_module