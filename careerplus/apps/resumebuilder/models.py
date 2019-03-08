# django imports
from django.db import models

# import from inter app
from seo.models import AbstractAutoDate

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


class UserProfile(AbstractAutoDate):
    first_name = models.CharField('User First Name', max_length=100, blank=True, null=True)
    last_name = models.CharField('User Last Name', max_length=100, blank=True, null=True)
    email = models.CharField('User Email', max_length=100, unique=True, blank=True, null=True)
    number = models.CharField('User Contact Number', max_length=15, blank=True, null=True)
    date_of_birth = models.DateField('DOB', blank=True, null=True)
    location = models.CharField('User Location', max_length=100, blank=True, null=True)
    image = models.FileField(upload_to='users/', null=True, blank=True)
    gender = models.CharField('Gender', choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Others')), max_length=1,
                              blank=True, null=True)
    extracurricular = models.CharField('Extra Curricular', max_length=50, blank=True, null=True,
                                       choices=INTERESTS)
    extra_info = models.TextField('Extra Information', blank=True, null=True)

    class Meta:
        abstract = True


class User(UserProfile):

    def __str__(self):
        return '{}-{}'.format(self.first_name, self.last_name)


class Skill(AbstractAutoDate):
    name = models.CharField('Skill Name', max_length=100)
    proficiency = models.IntegerField('Proficiency', default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return self.name


class UserExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    job_profile = models.CharField('Job Profile', max_length=100)
    company_name = models.CharField('Company Name', max_length=200)
    start_date = models.DateField('Start Date', blank=False)
    end_date = models.DateField('End Date', blank=True)
    is_working = models.BooleanField('Present')
    job_location = models.CharField('Job Location', max_length=100)
    work_description = models.TextField('Job Description')

    def __str__(self):
        return self.company_name


class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    specialization = models.CharField('Specialization', max_length=200)
    institution_name = models.CharField('Institution Name', max_length=250)
    course_type = models.CharField('Institution Name', choices=(('FT', 'Full Time'), ('PT', 'Part Time'),
                                                                ('CR', 'Correspondence')), max_length=2)
    percentage_cgpa = models.CharField('Percentage Or CGPA', max_length=250)
    start_date = models.DateField('Start Date', blank=False)
    end_date = models.DateField('End Date', blank=True)
    is_pursuing = models.BooleanField('Still Pursuing')

    def __str__(self):
        return self.specialization


class UserCertification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    name_of_certification = models.CharField('Certification Name', max_length=250)
    year_of_certification = models.DateField('Year of Certification')

    def __str__(self):
        return self.name_of_certification


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    project_name = models.CharField('Project Name', max_length=150)
    start_date = models.DateField('Start Date', blank=False)
    end_date = models.DateField('End Date', blank=True)
    skills = models.ManyToManyField(Skill, verbose_name='List of Skills', null=True, blank=True)
    description = models.TextField('Project Description')

    def __str__(self):
        return self.project_name


class UserReference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    reference_name = models.CharField('Reference Name', max_length=150)
    reference_designation = models.CharField('Reference Designation', max_length=150)
    about_user = models.TextField('About User')

    def __str__(self):
        return self.reference_name


class UserSocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    link_name = models.CharField('Link Name', max_length=10,
                                 choices=SOCIAL_LINKS)
    link = models.CharField('Link', max_length=200)

    def __str__(self):
        return self.link_name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    title = models.CharField('Title', max_length=100)
    date = models.DateField('Date')
    summary = models.TextField('Summary')

    def __str__(self):
        return self.title


class UserLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    name = models.CharField('Language Name', max_length=100)
    proficiency = models.IntegerField('Proficiency', default=3)

    def __str__(self):
        return self.name
