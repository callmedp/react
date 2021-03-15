# Python Core Import
import logging

# Django-Core Import
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404

# Inter-App Import
from core.common import APIResponse
from shop.views import ProductInformationMixin
from shop.models import (Product, Skill)
from .serializers import (
    ProductDetailSerializer)

# DRF Import
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


