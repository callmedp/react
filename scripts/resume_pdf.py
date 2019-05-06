# python imports
import os, django, sys
# django imports

from weasyprint import HTML, CSS

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")

#  setup django
django.setup()
from django.conf import settings
from django.template.loader import get_template
from resumebuilder.models import User

if __name__ == '__main__':
    # import ipdb;
    #
    # ipdb.set_trace();
    # user = User.objects.get(id=95)
    # extracurricular = user.extracurricular.split(',')
    # education = user.usereducation_set.all()
    # experience = user.userexperience_set.all()
    # skills = user.skill_set.all()
    # achievements = user.userachievement_set.all()
    # references = user.userreference_set.all()
    # projects = user.userproject_set.all()
    # certifications = user.usercertification_set.all()
    # languages = user.userlanguage_set.all()
    # current_exp = experience.filter(is_working=True).order_by('-start_date').first()

    # context_dict = {'user': user, 'education': education, 'experience': experience, 'skills': skills,
    #                 'achievements': achievements, 'references': references, 'projects': projects,
    #                 'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
    #                 'current_exp': current_exp}

    template = get_template('resume1.html')
    rendered_template = template.render({"is_pdf": True}).encode(encoding='UTF-8')
    print(rendered_template)
    HTML(string=rendered_template).write_pdf('test2.pdf', stylesheets=[CSS(string='@page {size:A3; margin:0px}')])
