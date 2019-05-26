# python imports
import json,ast

# django imports
from django.db import models
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

INTERESTS = ((0, '3D printing'), (1, 'Acrobatics'), (2, 'Acting'), (3, 'Amateur radio'), (4, 'Animation'),
             (5, 'Aquascaping'), (6, 'Baking'), (7, 'Baton twirling'), (8, 'Beatboxing'), (9, 'Board/tabletop games'),
             (10, 'Book restoration'), (11, 'Brazilian jiu-jitsu'), (12, 'Cabaret'), (13, 'Calligraphy'),
             (14, 'Candle making'), (15, 'Coffee roasting'), (16, 'Collecting'), (17, 'Coloring'),
             (18, 'Computer programming'), (19, 'Cooking'), (20, 'Cosplaying'), (21, 'Couponing'),
             (22, 'Creative writing'), (23, 'Crocheting'), (24, 'Cross-stitch'), (25, 'Crossword puzzles'),
             (26, 'Cryptography'), (27, 'Dance'), (28, 'Digital arts'), (29, 'Do it yourself'), (30, 'Drama'),
             (31, 'Drawing'), (32, 'Electronics'), (33, 'Embroidery'), (34, 'Fantasy sports'), (35, 'Fashion'),
             (36, 'Fishkeeping'), (37, 'Flower arranging'), (38, 'Foreign language learning'),
             (39, 'Gaming (tabletop games and role-playing games)'), (40, 'Genealogy'), (41, 'Glassblowing'),
             (42, 'Graphic design'), (43, 'Gunsmithing'), (44, 'Herp keeping'), (45, 'Homebrewing'),
             (46, 'Hydroponics'), (47, 'Ice skating'), (48, 'Jewelry making'), (49, 'Jigsaw puzzles'), (50, 'Juggling'),
             (51, 'Karate'), (52, 'Knife making'), (53, 'Knitting'), (54, 'Kombucha brewing'), (55, 'Lace making'),
             (56, 'Lapidary'), (57, 'Leather crafting'), (58, 'Lego building'), (59, 'Lock Picking'),
             (60, 'Listening to music'), (61, 'Machining'), (62, 'Macrame'), (63, 'Magic'), (64, 'Metalworking'),
             (65, 'Model building'), (66, 'Model engineering'), (67, 'Needlepoint'), (68, 'Origami'), (69, 'Painting'),
             (70, 'Philately'), (71, 'Photography'), (72, 'Playing musical instruments'), (73, 'Poi'), (74, 'Pottery'),
             (75, 'Puzzles'), (76, 'Quilling'), (77, 'Quilting'), (78, 'Reading'), (79, 'Robot combat'),
             (80, 'Scrapbooking'), (81, 'Sculpting'), (82, 'Sewing'), (83, 'Singing'), (84, 'Sketching'),
             (85, 'Soapmaking'), (86, 'Stand-up comedy'), (87, 'Taxidermy'), (88, 'Video game developing'),
             (89, 'Video gaming'), (90, 'Video editing'), (91, 'Watching movies'), (92, 'Watching television'),
             (93, 'Whittling'), (94, 'Wood carving'), (95, 'Woodworking'), (96, 'Worldbuilding'), (97, 'Writing'),
             (98, 'Yo-yoing'), (99, 'Yoga'))

interest_dict = dict(INTERESTS)


class CandidateProfile(AbstractAutoDate):
    candidate_id = models.CharField('Candidate Id', max_length=100, blank=True, null=True)
    first_name = models.CharField('Candidate First Name', max_length=100, blank=True, null=True)
    last_name = models.CharField('Candidate Last Name', max_length=100, blank=True, null=True)
    email = models.CharField('Candidate Email', max_length=100, unique=True, blank=True, null=True)
    number = models.CharField('Candidate Contact Number', max_length=15, blank=True, null=True)
    date_of_birth = models.DateField('DOB', blank=True, null=True)
    location = models.CharField('Candidate Location', max_length=100, blank=True, null=True)
    image = models.CharField('Candidate Image Url', max_length=200, blank=True, null=True)
    gender = models.CharField('Gender', choices=(('1', 'Male'), ('2', 'Female'), ('3', 'Others')), max_length=1,
                              blank=True, null=True)
    extracurricular = models.CharField('Extra Curricular', max_length=200, blank=True, null=True)
    selected_template = models.CharField('Selected Template', max_length=20, blank=True, null=True)
    extra_info = models.TextField('Extra Information', blank=True, null=True)
    entity_preference_data = models.TextField(blank=True, null=True)

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
            data[item.get('entity_id')] = {"active":item.get('active'),"entity_text":item.get("entity_text")}

        return data
    
    @property
    def extracurricular_list(self):
        return [interest_dict[int(x)] for x in self.extracurricular.split(',')] if self.extracurricular != '' else []

    class Meta:
        abstract = True


class Candidate(PreviewImageCreationMixin, CandidateProfile):
    parent_object_key = "id"

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
            update_customisations_for_all_templates.delay(self.id)

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

    @property
    def entity_position_eval(self):
        try:
            return json.loads(self.entity_position) 
        except:
            return []


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
    job_location = models.CharField('Job Location', max_length=100, blank=True, null=True)
    work_description = models.TextField('Job Description', blank=True, null=True)
    order = models.IntegerField('Order', default=0)

    @property
    def owner_id(self):
        return self.candidate.candidate_id

    def __str__(self):
        return self.company_name


class CandidateEducation(PreviewImageCreationMixin, models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Candidate')
    specialization = models.CharField('Specialization', max_length=200)
    institution_name = models.CharField('Institution Name', max_length=250)
    course_type = models.CharField('Institution Name', choices=(('FT', 'Full Time'), ('PT', 'Part Time'),
                                                                ('CR', 'Correspondence')), max_length=2)
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
    start_date = models.DateField('Start Date', blank=False)
    end_date = models.DateField('End Date', blank=True)
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
    title = models.CharField('Title', max_length=100)
    date = models.DateField('Date')
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
           CandidateAchievement, CandidateLanguage]

for model_name in senders:
    post_save.connect(model_name.preview_image_task_call, sender=model_name)




