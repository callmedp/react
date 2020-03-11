from django.db import models
from ckeditor.fields import RichTextField
from seo.models import AbstractAutoDate
from django.utils.translation import ugettext_lazy as _

LEVEL = ((-1, '---------'),(0, 'School'),(1,'College'),)


class Draft(AbstractAutoDate):
    """Draft for the linkedin course"""
    candidate_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Name')
    headline = models.CharField(max_length=120, verbose_name='Headline', null=True, blank=True)
    summary = RichTextField(verbose_name='Summary', null=True, blank=True)
    profile_photo = models.CharField(max_length=2000,null=True,
        blank=True, verbose_name='Profile Photograph')
    recommendation = models.CharField(max_length=2000,null=True,
        blank=True, verbose_name='Recommendations')
    follow_company = models.CharField(max_length=2000,null=True,
        blank=True, verbose_name='Follow Companies')
    join_group = models.CharField(max_length=2000,null=True,
        blank=True, verbose_name='Join Groups')
    public_url = models.CharField(max_length=2000,null=True,
        blank=True, verbose_name='Public Urls')
    key_skills = models.CharField(
        max_length=2000,
        null=True,
        blank=True,
        help_text='comma separated(,) separated skills, e.g. java, python, ...')

    cd_id = models.IntegerField(
        _('CP Draft'),
        blank=True,
        null=True,
        editable=False)

    def __str__(self):

        return str(self.pk)
 

class Organization(AbstractAutoDate):
    draft = models.ForeignKey(
        Draft, related_name='from_organization',on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Company Name')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Title')
    org_desc = RichTextField(verbose_name='Organization Description', null=True, blank=True)
    work_from = models.DateField(blank=True, null=True, verbose_name='From',help_text="Date Format MM/DD/YYYY")
    work_to = models.DateField(blank=True, null=True, verbose_name='To',help_text="Date Format MM/DD/YYYY")
    org_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Education(AbstractAutoDate):
    draft = models.ForeignKey(
        Draft, related_name='from_education',on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='School Name')
    level = models.PositiveSmallIntegerField(default=1, choices=LEVEL)
    degree = models.CharField(max_length=100, null=True, blank=True, verbose_name='Degree')
    edu_desc = RichTextField(verbose_name='Education Description', null=True, blank=True)
    field = models.CharField(max_length=100, null=True, blank=True, verbose_name='Field Of Study')
    study_from = models.DateField(blank=True, null=True, verbose_name='From',help_text="Date Format MM/DD/YYYY")
    study_to = models.DateField(blank=True, null=True, verbose_name='To',help_text="Date Format MM/DD/YYYY")
    edu_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)
