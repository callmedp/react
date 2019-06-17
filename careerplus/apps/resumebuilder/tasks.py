#python imports
import os,json
from io import BytesIO
from datetime import date

#django imports
from django.conf import settings
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile

#local imports

#inter app imports
from core.library.gcloud.custom_cloud_storage import GCPResumeBuilderStorage

#third party imports
import zipfile
import imgkit,pdfkit
from PIL import Image
from celery.decorators import task

@task
def generate_image_for_resume(candidate_id,template_no):
    from .models import Candidate
    from resumebuilder.utils import ResumeGenerator
    from resumebuilder.utils import store_resume_file

    candidate = Candidate.objects.filter(id=candidate_id).first()
    if not candidate:
        return

    thumbnail_sizes = [(151,249),(144,149)]
    
    current_config = candidate.ordercustomisation_set.filter(template_no=template_no).first()
    entity_position = current_config.entity_position_eval
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

    entity_id_count_mapping = {
                2:bool(education.count()),
                3:bool(experience.count()),
                4:bool(projects.count()),
                5:bool(skills.count()),
                7:bool(achievements.count()),
                8:bool(certifications.count()),
                9:bool(languages.count()),
                10:bool(references.count()),
                11:bool(len(extracurricular)),
            }
    updated_entity_position = []

    for item in entity_position:
        item.update({"count":entity_id_count_mapping.get(item['entity_id'])})
        updated_entity_position.append(item)

    generator_obj = ResumeGenerator()

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

    template = get_template('resume{}_preview.html'.format(template_no))
    current_config = candidate.ordercustomisation_set.filter(template_no=template_no).first()
    entity_position = current_config.entity_position_eval

    rendered_template = template.render(
        {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
        'achievements': achievements, 'references': references, 'projects': projects,
        'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
        'current_exp': current_exp, 'latest_exp': latest_experience,
        'preference_list': entity_preference,'current_config': current_config,
        'entity_position': updated_entity_position, 'width': 93.7, 'is_img': True
        }).encode(encoding='UTF-8')

    file_name = 'resumetemplate-' + str(template_no) + '.png'
    rendered_template = rendered_template.decode()
    rendered_template = rendered_template.replace("\n","")

    file = imgkit.from_string(rendered_template,False,{'quiet':''})
    in_mem_file = BytesIO(file)
    in_mem_file_to_upload = BytesIO()
    img = Image.open(in_mem_file)
    img = remove_transparency(img)
    img.save(in_mem_file_to_upload,"PNG")
    store_resume_file(str(candidate.id)+"/images",file_name,in_mem_file_to_upload.getvalue())

    for tsize in thumbnail_sizes:
        tname = "resumetemplate-{}-{}x{}.png".format(template_no,tsize[0],tsize[1])
        in_mem_file_to_upload = BytesIO()
        img.thumbnail(tsize,Image.ANTIALIAS)
        img.save(in_mem_file_to_upload, "PNG")
        store_resume_file(str(candidate.id)+"/images",tname,in_mem_file_to_upload.getvalue())


def remove_transparency(im,bg_colour=(255, 255, 255)):
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im
    
@task
def update_customisations_for_all_templates(candidate_id):
    from resumebuilder.models import Candidate, OrderCustomisation
    candidate_obj = Candidate.objects.get(id=candidate_id)
    customisation_objects = OrderCustomisation.objects.filter(candidate_id=candidate_id)
    entity_id_data_mapping = candidate_obj.entity_id_data_mapping
    entity_id_data_mapping[11] = {'active': True, 'entity_id': 11,'entity_text': "Interest",'priority': 11}

    for obj in customisation_objects:
        existing_data = obj.entity_position_eval
        data = []
        for item in existing_data:
            d = {key:value for key,value in item.items()}
            d['active'] = entity_id_data_mapping[d['entity_id']]['active']
            d['entity_text'] = entity_id_data_mapping[d['entity_id']]['entity_text']
            data.append(d)

        obj.entity_position = json.dumps(data)
        obj.save()

@task
def zip_all_resume_pdfs(order_id):
    from resumebuilder.models import Candidate
    from order.models import Order
    from resumebuilder.utils import store_resume_file

    order = Order.objects.get(id=order_id)

    content_type = "zip"
    candidate = Candidate.objects.get(candidate_id=order.candidate_id)
    file_dir = "{}/{}".format(candidate.id, content_type)
    file_name = "{}.{}".format("combo", content_type)

    zip_stream = BytesIO()
    zf = zipfile.ZipFile(zip_stream, "w")

    for i in range(1, 6):
        current_file = "{}_{}-{}.{}".format(order.first_name, order.last_name, i, "pdf")
        pdf_file_path = "{}/{}/pdf/{}.pdf".format(settings.RESUME_TEMPLATE_DIR, candidate.id, i)
        try:
            file_obj = GCPResumeBuilderStorage().open(pdf_file_path)
        except:
            logging.getLogger('error_log').error("Unable to open file - {}".format(pdf_file_path))

        if not settings.IS_GCP:
            pdf_file_path = "{}/{}".format(settings.MEDIA_ROOT, pdf_file_path)
            try:
                file_obj = open(pdf_file_path, "rb")
            except:
                logging.getLogger('error_log').error("Unable to open file - {}".format(pdf_file_path))
                continue

        open(current_file, 'wb').write(file_obj.read())
        zf.write(current_file)
        os.unlink(current_file)

    zf.close()
    store_resume_file(file_dir, file_name, zip_stream.getvalue())


@task
def generate_and_upload_resume_pdf(data):
    from resumebuilder.models import Candidate
    from order.models import Order
    from resumebuilder.utils import store_resume_file

    data = json.loads(data)
    order = Order.objects.get(id=data.get('order_id'))
    template_no = data.get('template_no')

    #Render PDF for context
    def generate_file(context_dict={}, template_src= None,file_type='pdf'):
        if not template_src:
            return None

        html_template = get_template(template_src)
        rendered_html = html_template.render(context_dict).encode(encoding='UTF-8')
        if file_type == 'pdf':
            options = {
                        'page-size': 'Letter',
                        'encoding': "UTF-8",
                        'no-outline': None,
                        'margin-top': '0.3in',
                        'margin-right': '0.2in',
                        'margin-bottom': '0.2in',
                        'margin-left': '0.2in',
                        'quiet': ''
                    }
            rendered_html = rendered_html.decode().replace("\n","")
            file = pdfkit.from_string(rendered_html,False,options=options)

        elif file_type == 'png':
            file = HTML(string=rendered_html).write_png()

        return file

    #Prepare Context for PDF generation
    content_type = "pdf"
    candidate_id = order.candidate_id
    template_id = int(template_no)
    candidate = Candidate.objects.filter(candidate_id=candidate_id).first()
    if not candidate:
        return {}

    file_dir = "{}/{}".format(candidate.id, content_type)
    file_name = "{}.{}".format(template_no, content_type)
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
    current_config = candidate.ordercustomisation_set.filter(template_no=template_id).first()
    entity_position = current_config.entity_position_eval

    entity_id_count_mapping = {
                2:bool(education.count()),
                3:bool(experience.count()),
                4:bool(projects.count()),
                5:bool(skills.count()),
                7:bool(achievements.count()),
                8:bool(certifications.count()),
                9:bool(languages.count()),
                10:bool(references.count()),
                11:bool(len(extracurricular)),
            }
    updated_entity_position = []

    for item in entity_position:
        item.update({"count":entity_id_count_mapping.get(item['entity_id'])})
        updated_entity_position.append(item)

    latest_experience,latest_end_date = '', None
    for exp in experience:
        if exp.is_working:
            latest_end_date = date.today()
            latest_experience = exp.job_profile
            break
        elif latest_end_date is None:
            latest_end_date = exp.end_date
            latest_experience = exp.job_profile
        else:
            if latest_end_date < exp.end_date:
                latest_end_date = exp.end_date
                latest_experience = exp.job_profile

    template = get_template('resume{}_preview.html'.format(template_id))
    context_dict = {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
                    'achievements': achievements, 'references': references, 'projects': projects,
                    'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
                    'current_exp': current_exp, 'latest_exp': latest_experience,
                    'preference_list': entity_preference, 'current_config': current_config,
                    'entity_position': updated_entity_position, "width": 93.7
                    }

    pdf_file = generate_file(context_dict=context_dict,\
        template_src='resume{}_preview.html'.format(template_no),file_type='pdf')

    store_resume_file(file_dir,file_name,pdf_file)
    
    if template_no == 5:
        zip_all_resume_pdfs.apply_async((order.id,),countdown=2)





