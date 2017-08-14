from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CPUser(models.Model):
	email = models.EmailField(
        _('email address'),
        max_length=255, blank=False)
	username = models.CharField(
        _('username'),
        max_length=255, blank=False)
	shine_id = models.CharField(
        _('shine_id'),
        max_length=255, blank=False)

	def __str__(self):
		return self.email