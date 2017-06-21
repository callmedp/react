from django.db import models
from ckeditor.fields import RichTextField
from order.models import OrderItem

LEVEL = ((0, 'School'),(1,'College'),)


class Draft(models.Model):
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
        max_length=500,
        null=True,
        blank=True,
        help_text='comma separated(,) separated skills, e.g. java, python, ...')

    def __str__(self):

        return self.candidate_name
 

class Organization(models.Model):
    draft = models.ForeignKey(
        Draft, related_name='from_organization')
    draft = models.ForeignKey(Draft)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Company Name')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Title')
    desc = RichTextField(verbose_name='Description', null=True, blank=True)
    work_from = models.DateField(blank=True, null=True, verbose_name='From',help_text="Date Format MM/DD/YYYY")
    work_to = models.DateField(blank=True, null=True, verbose_name='To',help_text="Date Format MM/DD/YYYY")
    current = models.BooleanField(default=False)

    def __str__(self):

        return self.name


class Education(models.Model):
    draft = models.ForeignKey(
        Draft, related_name='from_education')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='School Name')
    level = models.PositiveSmallIntegerField(default=1, choices=LEVEL)
    degree = models.CharField(max_length=100, null=True, blank=True, verbose_name='Degree')
    desc = RichTextField(verbose_name='Description', null=True, blank=True)
    field = models.CharField(max_length=100, null=True, blank=True, verbose_name='Field Of Study')
    study_from = models.DateField(blank=True, null=True, verbose_name='From',help_text="Date Format MM/DD/YYYY")
    study_to = models.DateField(blank=True, null=True, verbose_name='To',help_text="Date Format MM/DD/YYYY")
    current = models.BooleanField(default=False)

    def __str__(self):

        return self.name


class QuizResponse(models.Model):
    """QuizResponse Sent with Linked In"""
    oi = models.OneToOneField(OrderItem, default=None, null=True)
    submitted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    question1 = models.CharField(max_length=500, blank=True, verbose_name=('Question1'))
    anser1 = models.CharField(max_length=500, verbose_name='Answer1', blank=True)
    question2 = models.CharField(max_length=500, blank=True, verbose_name=('Question2'))
    anser2 = models.CharField(max_length=500, verbose_name='Answer2', blank=True)
    question3 = models.CharField(max_length=500, blank=True, verbose_name=('Question3'))
    anser3 = models.CharField(max_length=500, verbose_name='Answer3', blank=True)
    question4 = models.CharField(max_length=500, blank=True, verbose_name=('Question4'))
    anser4 = models.CharField(max_length=500, verbose_name='Answer4', blank=True)
    question5 = models.CharField(max_length=500, blank=True, verbose_name=('Question5'))
    anser5 = models.CharField(max_length=500, verbose_name='Answer5', blank=True)