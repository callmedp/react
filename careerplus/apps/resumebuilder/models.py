# python imports
import json, ast

# django imports
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_mysql.models.fields import JSONField

# local imports
from .choices import *
from .mixins import PreviewImageCreationMixin
from .tasks import update_customisations_for_all_templates
from .constants import TEMPLATE_DEFAULT_ENTITY_POSITION, TEMPLATE_ALLOW_LEFT_RIGHT_SWITCH

# inter app imports
from seo.models import AbstractAutoDate

# third party imports

SOCIAL_LINKS = ((1, 'LinkedIn'), (2, 'Github'), (3, 'Behance'), (4, 'Dribble'), (5, 'Keggle')
                , (6, 'NPM'), (7, 'Upwork'), (8, 'PyPI'), (9, 'Stack Overflow'))

interest_dict = dict(INTEREST_LIST)


class CandidateProfile(AbstractAutoDate):
    candidate_id = models.CharField('Candidate Id', max_length=100, blank=True, null=True)
    first_name = models.CharField('Candidate First Name', max_length=100, blank=True, null=True)
    last_name = models.CharField('Candidate Last Name', max_length=100, blank=True, null=True)
    email = models.CharField('Candidate Email', max_length=100, unique=True, blank=True, null=True)
    number = models.CharField('Candidate Contact Number', max_length=15, blank=True, null=True)
    date_of_birth = models.DateField('DOB', blank=True, null=True)
    location = models.CharField('Candidate Location', max_length=300, blank=True, null=True)
    image = models.CharField('Candidate Image Url', max_length=200, blank=True, null=True)
    gender = models.CharField('Gender', choices=(('1', 'Male'), ('2', 'Female'), ('3', 'Others')), max_length=1,
                              blank=True, null=True)
    extracurricular = models.TextField('Extra Curricular', blank=True, null=True)
    selected_template = models.CharField('Selected Template', max_length=20, blank=True, null=True)
    extra_info = models.TextField('Extra Information', blank=True, null=True)
    entity_preference_data = models.TextField(blank=True, null=True)
    upload_resume = models.BooleanField('Upload Resume', default=True)
    resume_generated = models.BooleanField('Resume Generated', default=True)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    @property
    def entity_id_data_mapping(self):
        try:
            entity_data = ast.literal_eval(self.entity_preference_data)
        except:
            return {}

        data = {}
        for item in entity_data:
            data[item.get('entity_id')] = {"active": item.get('active'), "entity_text": item.get("entity_text")}

        return data

    @property
    def extracurricular_list(self):
        return [x for x in self.extracurricular.split(',')] if self.extracurricular != '' else []

    class Meta:
        abstract = True


class Candidate(PreviewImageCreationMixin, CandidateProfile):
    parent_object_key = "id"
    initiate_image_upload_task = True

    @property
    def order_data(self):
        from order.models import Order

        product_found = False
        order_data = {}
        order_obj_list = Order.objects.filter(candidate_id=self.candidate_id, status__in=[1, 3])

        if not order_obj_list:
            return order_data

        for order_obj in order_obj_list:
            if product_found:
                break

            for item in order_obj.orderitems.all():
                if item.product and item.product.type_flow == 17 and item.product.type_product == 0:
                    order_data = {"id": order_obj.id,
                                  "combo": True if item.product.attr.get_value_by_attribute(item.product.attr.get_attribute_by_name('template_type')).value == 'multiple' else False
                                  }
                    product_found = True
                    break
        return order_data

    def create_template_customisations(self, candidate_id):
        for i in range(1, 6):
            obj = OrderCustomisation()
            obj.candidate_id = candidate_id
            obj.template_no = i
            obj.entity_position = json.dumps(TEMPLATE_DEFAULT_ENTITY_POSITION[i])
            obj.save()

    def save(self, **kwargs):
        created = not bool(getattr(self, "id"))
        obj = super(Candidate, self).save(**kwargs)

        if created:
            self.create_template_customisations(self.id)

        if not created:
            update_customisations_for_all_templates(self.id)

        return obj

    def __str__(self):
        return '{}-{}'.format(self.first_name, self.last_name)


class OrderCustomisation(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    template_no = models.SmallIntegerField(default=1)
    color = models.SmallIntegerField(choices=RESUME_COLOR_CHOICES, default=1)
    heading_font_size = models.SmallIntegerField(choices=RESUME_FONT_SIZE_CHOICES, default=1)
    text_font_size = models.SmallIntegerField(choices=RESUME_FONT_SIZE_CHOICES, default=1)
    entity_position = JSONField(blank=True, null=True)

    initiate_image_upload_task = True

    @property
    def entity_position_eval(self):
        try:
            return json.loads(self.entity_position)
        except:
            return []

    @property
    def entity_id_count_mapping(self):
        extracurricular = self.candidate.extracurricular_list
        education = self.candidate.candidateeducation_set.all().order_by('order')
        experience = self.candidate.candidateexperience_set.all().order_by('order')
        skills = self.candidate.skill_set.all().order_by('order')
        achievements = self.candidate.candidateachievement_set.all().order_by('order')
        references = self.candidate.candidatereference_set.all().order_by('order')
        projects = self.candidate.candidateproject_set.all().order_by('order')
        certifications = self.candidate.candidatecertification_set.all().order_by('order')
        languages = self.candidate.candidatelanguage_set.all().order_by('order')

        entity_id_count_mapping = {
            2: bool(education.count()),
            3: bool(experience.count()),
            4: bool(projects.count()),
            5: bool(skills.count()),
            7: bool(achievements.count()),
            8: bool(certifications.count()),
            9: bool(languages.count()),
            10: bool(references.count()),
            11: bool(len(extracurricular)),
        }

        return entity_id_count_mapping


class Skill(PreviewImageCreationMixin, AbstractAutoDate):
    name = models.CharField('Skill Name', max_length=100)
    proficiency = models.IntegerField('Proficiency', default=5)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.name


class CandidateExperience(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    job_profile = models.CharField('Job Profile', max_length=100)
    company_name = models.CharField('Company Name', max_length=200)
    start_date = models.DateField('Start Date', blank=True, null=True)
    end_date = models.DateField('End Date', blank=True, null=True)
    is_working = models.BooleanField('Present', default=False)
    job_location = models.CharField('Job Location', max_length=300, blank=True, null=True)
    work_description = models.TextField('Job Description', blank=True, null=True)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.company_name


class CandidateEducation(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    degree = models.CharField('Degree', max_length=200, blank=True, null=True)
    specialization = models.CharField('Specialization', max_length=200)
    institution_name = models.CharField('Institution Name', max_length=250)
    course_type = models.CharField('Institution Name', choices=(('FT', 'Full Time'), ('PT', 'Part Time'),
                                                                ('CR', 'Correspondence'), ('NA', 'NA')), max_length=2)
    percentage_cgpa = models.CharField('Percentage Or CGPA', max_length=250, null=True, blank=True)
    start_date = models.DateField('Start Date', blank=True, null=True)
    end_date = models.DateField('End Date', blank=True, null=True)
    is_pursuing = models.BooleanField('Still Pursuing', default=False)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.specialization


class CandidateCertification(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    name_of_certification = models.CharField('Certification Name', max_length=250)
    year_of_certification = models.IntegerField('Year of Certification')
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.name_of_certification


class CandidateProject(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    project_name = models.CharField('Project Name', max_length=150)
    start_date = models.DateField('Start Date', blank=False, null=True)
    end_date = models.DateField('End Date', blank=True, null=True)
    skills = models.ManyToManyField(Skill, verbose_name='List of Skills', null=True, blank=True)
    currently_working = models.BooleanField('Currently Working', default=False)
    description = models.TextField('Project Description', blank=True, null=True)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.project_name


class CandidateReference(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    reference_name = models.CharField('Reference Name', max_length=150)
    reference_designation = models.CharField('Reference Designation', max_length=150)
    about_candidate = models.TextField('About Candidate', null=True, blank=True)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.reference_name


class CandidateSocialLink(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    link_name = models.CharField('Link Name', max_length=10,
                                 choices=SOCIAL_LINKS)
    link = models.CharField('Link', max_length=200)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.link_name


class CandidateAchievement(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    title = models.CharField('Title', max_length=300)
    date = models.IntegerField('Date', blank=True, null=True)
    summary = models.TextField('Summary', null=True, blank=True)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.title


class CandidateLanguage(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    name = models.CharField('Language Name', max_length=100)
    proficiency = models.IntegerField('Proficiency', default=3)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.name


senders = [Candidate, Skill, CandidateExperience, CandidateEducation, \
           CandidateCertification, CandidateProject, CandidateReference, \
           CandidateAchievement, CandidateLanguage, OrderCustomisation]

for model_name in senders:
    post_save.connect(model_name.preview_image_task_call, sender=model_name)
