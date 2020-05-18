from seo.models import AbstractAutoDate
from django_mysql.models.fields import JSONField
from django.db import models

class ResumeScoreCheckerUserDetails(AbstractAutoDate):
    email = models.CharField(
        "Email", max_length=30, unique=True, 
        help_text=('Email extracted from resume'))
    mobile_number = models.CharField(
        "Mobile", max_length=20, blank=True, null=True,  
        help_text=('Mobile extracted from resume'))
    total_score = models.PositiveIntegerField(null=True, default=0)
    section_scores = JSONField(blank=True, null=True)

    def __str__(self):
        return self.email
