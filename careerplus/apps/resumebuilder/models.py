# django imports
from django.db import models

# import from inter app
from shop.models import AbstractAutoDate


class UserProfile(AbstractAutoDate):
    first_name = models.CharField('User First Name', max_length=100, blank=True, null=True)
    last_name = models.CharField('User Last Name', max_length=100, blank=True, null=True)
    email = models.CharField('User Email', max_length=100, unique=True, blank=True, null=True)
    number = models.CharField('User Contact Number', max_length=15, blank=True, null=True)
    date_of_birth = models.DateField('DOB', blank=True, null=True)
    location = models.CharField('User Location', max_length=100, blank=True, null=True)
    gender = models.CharField('Gender', choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Others')), max_length=1,
                              blank=True, null=True)
    extra_info = models.TextField('Extra Information', blank=True, null=True)

    class Meta:
        abstract = True


class User(UserProfile):

    def __str__(self):
        return '{}-{}'.format(self.first_name, self.last_name)


class Skill(AbstractAutoDate):
    name = models.CharField('Skill Name', max_length=100)
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


class ExternalLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    link_name = models.CharField('Link Name', max_length=100)
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
