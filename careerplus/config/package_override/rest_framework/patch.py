#python imports

#django imports

#local imports
from .utils import paginator

# inter app imports

# third party imports
from rest_framework.generics import GenericAPIView


def patch_drf_paginator():
	GenericAPIView.paginator = paginator