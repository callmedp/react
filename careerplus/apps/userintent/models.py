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
    preferred_role = models.CharField(max_length=200, unique=True, blank=True, null=True)
    current_job_title = models.CharField(max_length=200, unique=True, blank=True, null=True)
    preferred_location = models.CharField(
        'Candidate Location', max_length=300, blank=True, null=True)
    experience = models.IntegerField(
        blank=True,
        null=True,
        editable=False)
    department = models.ForeignKey(FunctionalArea,on_delete=models.DO_NOTHING,
        to_field="id",
        null=True,
        blank=True,
        verbose_name=_("Department"))
    skills = models.ForeignKey(
        Skill,
        verbose_name=_('Skill'),
        on_delete=models.CASCADE,
        blank=True, null=True)
