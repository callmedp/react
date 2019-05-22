from celery.decorators import task
from django.template.loader import get_template
from weasyprint import HTML, CSS
from datetime import date
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

@task
def generate_image_for_resume(candidate_id):
    from .models import Candidate
    from core.mixins import ResumeGenerate
    candidate = Candidate.objects.filter(id=candidate_id).first()
    if not candidate:
        return {}

    entity_preference = eval(candidate.entity_preference_data)
    extracurricular = candidate.extracurricular_list
    education = candidate.candidateeducation_set.all().order_by('order')
    experience = candidate.candidateexperience_set.all().order_by('order')
    skills = candidate.skill_set.all().order_by('order')
    achievements = candidate.candidateachievement_set.all().order_by('order')
    references = candidate.candidatereference_set.all().order_by('order')
    projects = candidate.candidateproject_set.all().order_by('order')
    certifications = candidate.candidatecertification_set.all().order_by('order')
    languages = candidate.candidatelanguage_set.all().order_by('order')
    current_exp = experience.filter(is_working=True).order_by('-start_date').first()

    latest_experience, latest_end_date = '', None
    for i in experience:
        if i.is_working:
            latest_end_date = date.today()
            latest_experience = i.job_profile
            break
        elif latest_end_date == None:
            latest_end_date = i.end_date
            latest_experience = i.job_profile
        else:
            if latest_end_date < i.end_date:
                latest_end_date = i.end_date
                latest_experience = i.job_profile

    #latest_experience = experience and experience[0].job_profile or 'FULL STACK DEVELOPER'
    for i in range(1,6):
        template = get_template('resume{}.html'.format(i))
        rendered_template = template.render(
            {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
            'achievements': achievements, 'references': references, 'projects': projects,
  
            'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
            'current_exp': current_exp, 'latest_exp': latest_experience,
            'preference_list': entity_preference,
            }).encode(encoding='UTF-8')
        file_name = 'resumetemplate-' + str(i) + '.png'
        file = HTML(string=rendered_template).write_png(stylesheets=[CSS(string='@page {size:A3; margin:0px}')])
        from io import BytesIO
        # image = Image.frombytes('RGBA', (128,128), file, 'raw')
        img = Image.open(BytesIO(file))
        img = remove_transparency(img)
        img.save(file_name,"PNG")

        
       
        file_dir='images/'+str(candidate_id)
    
        file =open(file_name, 'rb')
        
        ResumeGenerate().store_file(file_dir, file_name, file)

def remove_transparency(im, bg_colour=(255, 255, 255)):

    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im
    
