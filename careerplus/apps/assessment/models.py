#python imports
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_mysql.models import JSONField
from django.utils.text import slugify



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
    slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True)
    title = models.CharField(
        max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    duration = models.PositiveSmallIntegerField(default=0)
    max_attempts = models.PositiveSmallIntegerField(default=3)
    passing_marks = models.PositiveSmallIntegerField(blank=True, null=True)
    max_score = models.PositiveSmallIntegerField(blank=True, null=True)
    instructions = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True,on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, null=True, blank=True,related_name='testcategories')
    course = models.ForeignKey(Product, null=True, blank=True,
                               related_name='testcourse',on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + "-" + str(self.max_score)

    def get_all_categories(self):
        cat_ids = set()
        if self.category:
            cat_ids.add(self.category.id)
        scat_ids = set(self.categories.values_list('id', flat=True)\
            .exclude(categories=None))
        return list(filter(None,cat_ids|scat_ids))

    def get_question_count(self):
        return self.question_set.all().count()

    def get_absolute_url(self):
        return "/practice-tests/{}-test/".format(self.slug)

    @property
    def question_count(self):
        return self.get_question_count()

    def save(self,*args,**kwargs):
        created = not bool(getattr(self, "id"))
        if not created:
            title = self.title
            value = slugify(getattr(self, 'slug') or title)
            self.slug = value
        super().save(*args, **kwargs)


class Section(AbstractAutoDate):
    name = models.CharField(
        max_length=255, null=False, blank=False)
    duration = models.PositiveSmallIntegerField(default=0)
    test = models.ForeignKey(Test,blank=True, null=True,on_delete=models.CASCADE)

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
    marks = models.FloatField(default=1)
    negative_marks = models.FloatField(default=0.00)
    test = models.ForeignKey(Test, blank=True, null=True,on_delete=models.CASCADE)
    section = models.ForeignKey(Section, blank=True, null=True,on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=LEVELS_TYPE,default=1)
    question_type = models.PositiveSmallIntegerField(choices=QUESTION_TYPE,default=1)
    subsection = models.ForeignKey(SubSection,blank=True,null=True,on_delete=models.CASCADE)
    question_options = models.TextField(null=True,blank=True)
    extra_info = models.CharField(
        max_length=255, null=False, blank=False,default="")


    @property
    def correct_option(self):
        return [option.get('option_id') for option in self.options\
                if option.get('is_correct') and bool(eval(option.get('is_correct'))\
                if isinstance(option.get('is_correct'), str) else option.get('is_correct'))]


    @property
    def options(self):
        if not self.question_options:
            return []
        try:
            value = eval(self.question_options)
        except Exception as e:
            logging.getLogger('error_log').error('unable to parse question '
                                                 'option id={}'.format(self.id))
            value =[]

        if not isinstance(value, list):
            return []

        if not all(isinstance(option, dict) for option in value):
            return []

        return value

    def __str__(self):
        return '{}'.format(self.id)






