from django.db import models
from seo.models import AbstractAutoDate
from django.utils.translation import ugettext_lazy as _


#inter app imports
from shop.models import FunctionalArea, Skill
from .choices import INTENT_CHOICES

# Create your models here.
class UserIntent(AbstractAutoDate):
    """
    Capture user intent like career_change, career_progress, findjob and improve_profile.
    """
    candidate_id = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_("Customer ID"))
    intent = models.PositiveSmallIntegerField(
        default=0, choices=INTENT_CHOICES)
    current_job_title = models.CharField(max_length=100, blank=True, null=True)
    preferred_role = models.CharField(max_length=200, blank=True, null=True)
    preferred_location = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    experience = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return dict(INTENT_CHOICES).get(self.intent)

class RecommendationFeedback(AbstractAutoDate):
    """
    captures if the user found the recommendations made useful or not.
    """
    candidate_id = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_("Customer ID"))
    intent = models.PositiveSmallIntegerField(
        default=0, choices=INTENT_CHOICES)
    recommendation_relevant = models.BooleanField(default=False)
    recommended_products = models.TextField(blank=True,null=True)
    context = models.CharField(max_length=100, blank=True, null=True)
