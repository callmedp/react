from django.db import models
from django.conf import settings
# Create your models here.


class AbstractCommonModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
        blank=True, related_name="%(app_label)s_%(class)s_created_by",
        related_query_name="%(app_label)s_%(class)ss",on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
        blank=True, related_name="%(app_label)s_%(class)s_last_modified_by",
        related_query_name="%(app_label)s_%(class)ss",on_delete=models.PROTECT)
    last_modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
