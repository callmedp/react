from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import JSONField


from shop.models import Category,Product
from partner.models import Vendor
from seo.models import AbstractAutoDate

LEVELS_TYPE = (
    (1, "Basic"),
    (2, "Intermediate"),
    (3,  "Advanced"),
    (5,  "N.A")
)
QUESTION_TYPE = (
    (1, "MCQ(SINGLE)"),
    (2, "MCQ(MULTIPLE)"),
)


class Test(AbstractAutoDate):
    title = models.CharField(
        max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    duration = models.PositiveSmallIntegerField(default=0)
    max_attempts = models.PositiveSmallIntegerField(default=3)
    passing_marks = models.PositiveSmallIntegerField(blank=True, null=True)
    max_score = models.PositiveSmallIntegerField(blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    vendor = models.ForeignKey(Vendor,blank=True, null=True)

    def __str__(self):
        return self.title + "-" + str(self.max_score)


class Section(AbstractAutoDate):
    name = models.CharField(
        max_length=255, null=False, blank=False)
    duration = models.PositiveSmallIntegerField(default=0)
    test = models.ForeignKey(Test,blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def weight(self):
        pass

    def get_questions(self):
        pass

class SubSection(AbstractAutoDate):

    paragraph = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)


class Question(AbstractAutoDate):

    question_text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    weight = models.PositiveSmallIntegerField(default=1)
    negative_marking = models.FloatField(default=0.00)
    test = models.ForeignKey(Test, blank=True, null=True)
    section = models.ForeignKey(Section, blank=True, null=True)
    level = models.PositiveSmallIntegerField(choices=LEVELS_TYPE,default=1)
    question_type = models.PositiveSmallIntegerField(choices=QUESTION_TYPE,default=1)
    subsection = models.ForeignKey(SubSection,blank=True,null=True)
    question_options = JSONField()
    extra_info = models.CharField(
        max_length=255, null=False, blank=False,default="")


    @property
    def correct_option(self):
        return [option.get('option_id') for option in self.question_options\
                if option.get('is_correct') and bool(eval(option.get('is_correct'))\
                if isinstance(option.get('is_correct'), str) else option.get('is_correct'))]
    #
    # @property
    # def get_option_list(self):



