# python imports
import os
import json
import sys
from io import BytesIO
from datetime import date
import logging

# django imports
from django.conf import settings
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile

# local imports
from .constants import ENTITY_LIST

# inter app imports
from core.library.gcloud.custom_cloud_storage import GCPResumeBuilderStorage
# third party imports
import zipfile
import imgkit
import pdfkit
from PIL import Image
from celery.decorators import task


@task
def generate_image_for_resume(candidate_id, template_no):
    from .models import Candidate
    from resumebuilder.utils import ResumeGenerator
    from resumebuilder.utils import store_resume_file

    candidate = Candidate.objects.filter(id=candidate_id).first()
    if not candidate:
        return

    thumbnail_sizes = [(151, 249), (144, 149)]

    current_config = candidate.ordercustomisation_set.filter(
        template_no=template_no).first()
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
    current_exp = experience.filter(
        is_working=True).order_by('-start_date').first()

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
    updated_entity_position = []

    for item in entity_position:
        item.update({"count": entity_id_count_mapping.get(item['entity_id'])})
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

    template_id_suffix_mapping = {1: "pdf", 4: "pdf"}
    template = get_template('resume{}_{}.html'.format(
        template_no, template_id_suffix_mapping.get(int(template_no), "preview")))

    rendered_template = template.render(
        {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
         'achievements': achievements, 'references': references, 'projects': projects,
         'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
         'current_exp': current_exp, 'latest_exp': latest_experience,
         'preference_list': entity_preference, 'current_config': current_config,
         'entity_position': updated_entity_position, 'width': 100, 'activate_water_mark': True
         }).encode(encoding='UTF-8')

    file_name = 'resumetemplate-' + str(template_no) + '.jpg'
    rendered_template = rendered_template.decode()
    # rendered_template = rendered_template.replace("\n", "")

    file = imgkit.from_string(rendered_template, False, {
                              'quiet': '', 'quality': '80', 'format': 'JPG'})
    in_mem_file = BytesIO(file)
    in_mem_file_to_upload = BytesIO()
    img = Image.open(in_mem_file)
    img = remove_transparency(img)
    img.save(in_mem_file_to_upload, "JPEG", quality=80)
    store_resume_file(str(candidate.id) + "/images",
                      file_name, in_mem_file_to_upload.getvalue())

    for tsize in thumbnail_sizes:
        tname = "resumetemplate-{}-{}x{}.jpg".format(
            template_no, tsize[0], tsize[1])
        in_mem_file_to_upload = BytesIO()
        img.thumbnail(tsize, Image.ANTIALIAS)
        img.save(in_mem_file_to_upload, "JPEG", quality=80)
        store_resume_file(str(candidate.id) + "/images",
                          tname, in_mem_file_to_upload.getvalue())


def remove_transparency(im, bg_colour=(255, 255, 255)):
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", im.size, bg_colour + (255,), quality=80)
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im


@task
def update_customisations_for_all_templates(candidate_id):
    from resumebuilder.models import Candidate, OrderCustomisation
    candidate_obj = Candidate.objects.get(id=candidate_id)
    customisation_objects = OrderCustomisation.objects.filter(
        candidate_id=candidate_id)
    entity_id_data_mapping = candidate_obj.entity_id_data_mapping
    entity_id_data_mapping[11] = {
        'active': True, 'entity_id': 11, 'entity_text': "Interest", 'priority': 11}

    for obj in customisation_objects:
        existing_data = obj.entity_position_eval
        data = []
        for item in existing_data:
            #d = {key: value for key, value in item.items()}
            #d['active'] = entity_id_data_mapping[d['entity_id']]['active']
            #d['entity_text'] = entity_id_data_mapping[d['entity_id']]['entity_text']
            if entity_id_data_mapping.get(item['entity_id'] )and entity_id_data_mapping[item['entity_id']].get('active'):
                item['active'] = True
            else:
                item['active'] = False

            if entity_id_data_mapping.get(item['entity_id']) and entity_id_data_mapping[item['entity_id']].get(
                    'entity_text'):
                item['active'] = entity_id_data_mapping[item['entity_id']].get('entity_text')
            else:
                item['active'] = ""
            data.append(item)

        obj.entity_position = json.dumps(data)
        obj.save()


@task
def zip_all_resume_pdfs(order_id, data):
    from resumebuilder.models import Candidate
    from order.models import Order
    from resumebuilder.utils import store_resume_file
    from order.tasks import send_resume_in_mail_resume_builder

    order = Order.objects.get(id=order_id)
    content_type = "zip"
    candidate = Candidate.objects.get(candidate_id=order.candidate_id)
    file_dir = "{}/{}".format(candidate.id, content_type)
    file_name = "{}.{}".format("combo", content_type)

    zip_stream = BytesIO()
    zf = zipfile.ZipFile(zip_stream, "w")

    for i in range(1, 6):
        current_file = "{}_{}-{}.{}".format(order.first_name,
                                            order.last_name, i, "pdf")
        pdf_file_path = "{}/{}/pdf/{}.pdf".format(
            settings.RESUME_TEMPLATE_DIR, candidate.id, i)
        try:
            file_obj = GCPResumeBuilderStorage().open(pdf_file_path)
        except:
            logging.getLogger('error_log').error(
                "Unable to open file - {}".format(pdf_file_path))

        if not settings.IS_GCP:
            pdf_file_path = "{}/{}".format(settings.MEDIA_ROOT, pdf_file_path)
            try:
                file_obj = open(pdf_file_path, "rb")
            except:
                logging.getLogger('error_log').error(
                    "Unable to open file - {}".format(pdf_file_path))
                continue

        open(current_file, 'wb').write(file_obj.read())
        zf.write(current_file)
        os.unlink(current_file)
    zf.close()
    store_resume_file(file_dir, file_name, zip_stream.getvalue())
    send_resume_in_mail_resume_builder(
        [file_name, zip_stream.getvalue()], data)

@task
def generate_and_upload_resume_pdf(data):
    from resumebuilder.models import Candidate, CandidateResumeOperations
    from order.models import Order
    from resumebuilder.utils import store_resume_file
    from order.tasks import send_resume_in_mail_resume_builder
    from core.api_mixin import UploadResumeToShine
    data = json.loads(data)
    order = Order.objects.filter(id=data.get('order_id')).first()
    template_no = data.get('template_no')
    send_mail = data.get('send_mail')
    is_free_trial = data.get('is_free_trial', False)
    is_combo = data.get('is_combo', False)

    #  check if order contains resume builder subscription
    def order_contains_resumebuilder_subscription():
        items = order.orderitems.all()
        return any([item.product.sub_type_flow == 1701 for item in items])

    def order_contains_expert_assistance():
        items = order.orderitems.all()
        return any([item.product.sub_type_flow == 101 for item in items])

    # Render PDF for context
    def generate_file(context_dict={}, template_src=None, file_type='pdf'):
        if not template_src:
            return None

        html_template = get_template(template_src)
        rendered_html = html_template.render(
            context_dict).encode(encoding='UTF-8')
        rendered_html = rendered_html.decode()

        if file_type == 'pdf':
            options = {
                'page-size': 'Letter',
                'encoding': "UTF-8",
                # 'no-outline': None,
                # 'margin-top': '0in',
                # 'margin-right': '0in',
                # 'margin-bottom': '0in',
                # 'margin-left': '0in',
                'image-dpi': 135,
                'quiet': '',
            }

            # rendered_html = rendered_html.decode().replace("\n", "")
            file = pdfkit.from_string(rendered_html, False, options=options)

        elif file_type == 'png':
            file = HTML(string=rendered_html).write_png()

        return file

    # Prepare Context for PDF generation
    content_type = "pdf"
    candidate_id = order.candidate_id if not is_free_trial else data.get(
        'candidate_id', '')

    if not candidate_id:
        logging.getLogger('error_log').error("No candidate id.")
        return

    template_id = int(template_no)
    candidate = Candidate.objects.using('master').filter(candidate_id=candidate_id).first()
    first_save = False

    if not candidate and not is_free_trial:
        candidate = Candidate.objects.create(
            email=order.email,
            number=order.mobile,
            candidate_id=candidate_id,
            extracurricular="",
            entity_preference_data=str(ENTITY_LIST),
            resume_generated=not order_contains_expert_assistance(),
            selected_template=1,
            active_subscription=order_contains_resumebuilder_subscription()
        )
        first_save = True
        candidate.save()
    elif not candidate and is_free_trial:
        logging.getLogger('error_log').error(
            "No candidate for this trial resume download.")
        return

    file_dir = "{}/{}".format(candidate.id, content_type)
    if is_free_trial:
        file_name = "free-trial-{}.{}".format(template_no, content_type)
    else:
        file_name = "{}.{}".format(template_no, content_type)

    entity_preference = eval(candidate.entity_preference_data or "{}")
    extracurricular = candidate.extracurricular_list
    education = candidate.candidateeducation_set.all().order_by('order')
    experience = candidate.candidateexperience_set.all().order_by('order')
    skills = candidate.skill_set.all().order_by('order')
    achievements = candidate.candidateachievement_set.all().order_by('order')
    references = candidate.candidatereference_set.all().order_by('order')
    projects = candidate.candidateproject_set.all().order_by('order')
    certifications = candidate.candidatecertification_set.all().order_by('order')
    languages = candidate.candidatelanguage_set.all().order_by('order')
    current_exp = experience.filter(
        is_working=True).order_by('-start_date').first()
    current_config = candidate.ordercustomisation_set.filter(
        template_no=template_id).first()
    entity_position = current_config.entity_position_eval

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
    updated_entity_position = []

    for item in entity_position:
        item.update({"count": entity_id_count_mapping.get(item['entity_id'])})
        updated_entity_position.append(item)

    latest_experience, latest_end_date = '', None
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

    template_id_suffix_mapping = {1: "pdf", 4: "pdf"}
    template_src = 'resume{}_{}.html'.format(
        template_id, template_id_suffix_mapping.get(template_id, "preview"))

    context_dict = {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
                    'achievements': achievements, 'references': references, 'projects': projects,
                    'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
                    'current_exp': current_exp, 'latest_exp': latest_experience,
                    'preference_list': entity_preference, 'current_config': current_config,
                    'entity_position': updated_entity_position, "width": 93.7
                    }
    pdf_file = generate_file(context_dict=context_dict,
                             template_src=template_src, file_type='pdf')

    for i in range(5):
        try:
            store_resume_file(file_dir, file_name, pdf_file)
            break
        except Exception as e:
            logging.getLogger('error_log').error("File not uploaded to cloud")

    if is_free_trial:
        op_status = 1  # for free resume creation operation status
        candidate.resume_creation_count += 1
        candidate.save()
        logging.getLogger('info_log').info(
            "Trial part finished and incremented download count")
    else:
        op_status = 2  # paid resume creation operation status

    data = {}
    data.update({
        'email': candidate.email,
        'username': candidate.first_name or "User",
        'subject': 'Your resume is here',
        'siteDomain': settings.SITE_DOMAIN
    })

    if template_no == 5 and is_combo:
        zip_all_resume_pdfs.apply_async((order.id, data), countdown=2)

    if send_mail:
        send_resume_in_mail_resume_builder(['resume', pdf_file], data)

    CandidateResumeOperations.objects.create(
        candidate=candidate, order=order, op_status=op_status)
    logging.getLogger('info_log').info(
        "RESUME BUILDER: File creation operation created for with op_status {}.".format(op_status))

    # uploading resume on the shine
    if template_id == int(candidate.selected_template or 0) and candidate.upload_resume and not first_save:
        info = {
            'candidate_id': candidate_id,
            'upload_medium': 'direct',
            'upload_source': 'web',
            'resume_source': 7,
            'resume_medium': 5,
            'resume_trigger': 7
        }
        resume_files = {
            'resume_file': pdf_file
        }
        response = UploadResumeToShine().sync_candidate_resume_to_shine(
            candidate_id=candidate_id, files=resume_files, data=info)
        if response:
            logging.getLogger('info_log').info(
                "RESUME BUILDER: Upload to shine successful.")
            return
        logging.getLogger('info_log').info(
            "RESUME BUILDER: Upload to shine failed.")
