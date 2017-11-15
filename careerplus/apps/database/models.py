from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

# class CPUser(models.Model):
#         cp_id = models.CharField(
#         _('cpid'),
#         max_length=255, blank=True)
#         email = models.EmailField(
#         _('email address'),
#         max_length=255, blank=True)
#         username = models.CharField(
#         _('username'),
#         max_length=255, blank=True)
#         shine_id = models.CharField(
#         _('shine_id'),
#         max_length=255, blank=True)
#         mobile = models.CharField(
#         _('mobile'),
#         max_length=255, blank=True)
#         country = models.CharField(
#         _('country'),
#         max_length=255, blank=True)
        
#         def __str__(self):
#                 return self.email