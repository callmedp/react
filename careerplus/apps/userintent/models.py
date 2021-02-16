from django.db import models
from seo.models import AbstractAutoDate
from django.utils.translation import ugettext_lazy as _


#inter app imports
from shop.models import FunctionalArea, Skill
from .choices import INTENT_CHOICES

# Create your models here.
class UserIntent(AbstractAutoDate):
    candidate_id = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_("Customer ID"))
    intent = models.PositiveSmallIntegerField(
        default=0, choices=INTENT_CHOICES)
    current_job_title = models.CharField(max_length=255, blank=True, null=True)
    preferred_role = models.TextField(blank=True,null=True)
    preferred_location = models.TextField(blank=True,null=True)
    department = models.TextField(blank=True,null=True)
    skills = models.TextField(blank=True,null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return dict(INTENT_CHOICES).get(self.intent)
