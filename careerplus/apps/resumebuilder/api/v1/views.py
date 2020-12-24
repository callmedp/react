# python imports
import base64, json, logging
import random
from datetime import datetime, date

# django imports
from django.conf import settings
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile
from django_redis import get_redis_connection
from django.http import HttpResponse


# local imports
from resumebuilder.models import (Candidate, Skill, CandidateExperience, CandidateEducation, CandidateCertification,
                                  CandidateProject, CandidateReference, CandidateSocialLink, CandidateAchievement,
                                  CandidateLanguage, OrderCustomisation)
from resumebuilder.api.core.serializers import (CandidateSerializer, SkillSerializer, CandidateExperienceSerializer,
                                                CandidateEducationSerializer, CandidateCertificationSerializer,
                                                CandidateProjectSerializer, CandidateAchievementSerializer,
                                                CandidateReferenceSerializer, CandidateSocialLinkSerializer,
                                                CandidateLanguageSerializer, OrderCustomisationSerializer)
from resumebuilder.choices import (INTEREST_LIST)
from resumebuilder.mixins import (SessionManagerMixin)
from resumebuilder.constants import EDUCATION_PARENT_CHILD_HEIRARCHY_LIST, JOB_TITLES
from resumebuilder.utils import ResumeEntityReorderUtility
from core.library.gcloud.custom_cloud_storage import GCPResumeBuilderStorage

# inter app imports
from shine.core import ShineCandidateDetail
from shared.rest_addons.authentication import ShineUserAuthentication
from shared.permissions import IsObjectOwner
from core.library.gcloud.custom_cloud_storage import GCPResumeBuilderStorage

# third party imports
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView)
from rest_framework.views import APIView
from rest_framework.parsers import (FormParser, MultiPartParser)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wsgiref.util import FileWrapper
import imgkit


class CandidateCreateView(CreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateCreateView, self).get_serializer(*args, **kwargs)


class CandidateRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    """
    PATCH for entity update - <br><br>

    {"entity_preference_data":
        [
            {
                "entity_id":2,
                "entity_text":"Type 2",
                "active":true,
                "priority":1
            },
            {
                "entity_id":3,
                "entity_text":"Entity 3",
                "active":true,
                "priority":2
            }
        ]
    }
    """
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    lookup_field = 'candidate_id'
    lookup_url_kwarg = 'pk'
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()


class SkillListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SkillSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return Skill.objects.filter(candidate__in=candidate_obj).order_by(
            'order')

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(SkillListCreateView, self).get_serializer(*args, **kwargs)


class SkillRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "pk"


class CandidateExperienceListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateExperienceSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    # def get_queryset(self):
    #     candidate_id = self.request.GET.get('c_id', '')
    #     if 'candidate_experience' not in self.request.session:
    #         candidate = Candidate.objects.get(candidate_id=candidate_id)
    #         return candidate.candidateexperience_set.all()

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateExperience.objects.filter(
            candidate__in=candidate_obj).order_by('order')

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateExperienceListCreateView, self).get_serializer(*args, **kwargs)


class CandidateExperienceRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateExperienceSerializer

    def get_queryset(self):
        candidate_experience_id = int(self.kwargs.get('pk'))
        return CandidateExperience.objects.filter(id=candidate_experience_id)


class CandidateEducationListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateEducationSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateEducation.objects.filter(candidate__in=candidate_obj)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateEducationListCreateView, self).get_serializer(*args, **kwargs)


class CandidateEducationRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateEducationSerializer

    def get_queryset(self):
        candidate_education_id = int(self.kwargs.get('pk'))
        return CandidateEducation.objects.filter(id=candidate_education_id)


class CandidateCertificationListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateCertificationSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateCertification.objects.filter(
            candidate__in=candidate_obj).order_by('order')

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateCertificationListCreateView, self).get_serializer(*args, **kwargs)


class CandidateCertificationRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateCertificationSerializer

    def get_queryset(self):
        candidate_certification_id = int(self.kwargs.get('pk'))
        return CandidateCertification.objects.filter(id=candidate_certification_id)


class CandidateProjectListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateProjectSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateProjectListCreateView, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateProject.objects.filter(
            candidate__in=candidate_obj).order_by('order')


class CandidateProjectRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateProjectSerializer

    def get_queryset(self):
        candidate_project_id = int(self.kwargs.get('pk'))
        return CandidateProject.objects.filter(id=candidate_project_id)


class CandidateReferenceListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateReferenceSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateReferenceListCreateView, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateReference.objects.filter(
            candidate__in=candidate_obj).order_by('order')


class CandidateReferenceRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateReferenceSerializer

    def get_queryset(self):
        candidate_reference_id = int(self.kwargs.get('pk'))
        return CandidateReference.objects.filter(id=candidate_reference_id)


class CandidateSocialLinkListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateSocialLinkSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateSocialLinkListCreateView, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateSocialLink.objects.filter(
            candidate__in=candidate_obj).order_by('order')


class CandidateSocialLinkRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateSocialLinkSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return CandidateSocialLink.objects.filter(id=external_link_id)


class CandidateAchievementListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateAchievementSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateAchievementListCreateView, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateAchievement.objects.filter(
            candidate__in=candidate_obj).order_by('order')


class CandidateAchievementRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateAchievementSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return CandidateAchievement.objects.filter(id=external_link_id)


class CandidateLanguageListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CandidateLanguageSerializer
    ordering_fields = ('order',)
    ordering = ('order',)

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id)
        return CandidateLanguage.objects.filter(
            candidate__in=candidate_obj).order_by('order')

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateLanguageListCreateView, self).get_serializer(*args, **kwargs)


class CandidateLanguageRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = CandidateLanguageSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return CandidateLanguage.objects.filter(id=external_link_id)


class CandidateResumePreview(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        candidate_id = self.kwargs.get('candidate_id', '')
        template_id = self.kwargs.get('pk', '')
        candidate = Candidate.objects.filter(candidate_id=candidate_id).first()
        if not candidate:
            return Response({})
        current_config = candidate.ordercustomisation_set.filter(template_no=template_id).first()
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

        template = get_template('resume{}_preview.html'.format(template_id))
        rendered_template = template.render(
            {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
             'achievements': achievements, 'references': references, 'projects': projects,
             'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
             'current_exp': current_exp, 'latest_exp': latest_experience,
             'preference_list': entity_preference, 'current_config': current_config,
             'entity_position': updated_entity_position, 'width': 100, "watermark_in_preview": True
             }).encode(encoding='UTF-8')

        return Response({
            'html': rendered_template
        })


class ProfileEntityBulkUpdateView(APIView):
    """
    Expected behaviour - 

    http://127.0.0.1:8000/api/v1/resume/candidate/5c4ede4da4d7330573d8c79b/bulk-update/skill/

    Sample input data - 

    [{
        "candidate_id": "1",
        "cc_id": null,
        "name": "Java",
        "proficiency": 2
    },

    {   "id":1,
        "candidate_id": "1",
        "cc_id": null,
        "name": "Django",
        "proficiency": 2
    }]

    Output - 

    [{  "id":2,
        "candidate_id": "1",
        "cc_id": null,
        "name": "Java",
        "proficiency": 2
    },

    {   "id":1,
        "candidate_id": "1",
        "cc_id": null,
        "name": "Django",
        "proficiency": 2
    }]
    """
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    entity_slug_serializer_mapping = {'skill': SkillSerializer,
                                      'experience': CandidateExperienceSerializer,
                                      'education': CandidateEducationSerializer,
                                      'certification': CandidateCertificationSerializer,
                                      'project': CandidateProjectSerializer,
                                      'reference': CandidateReferenceSerializer,
                                      'social-link': CandidateSocialLinkSerializer,
                                      'language': CandidateLanguageSerializer,
                                      'achievement': CandidateAchievementSerializer}

    entity_slug_model_mapping = {'skill': Skill,
                                 'experience': CandidateExperience,
                                 'education': CandidateEducation,
                                 'certification': CandidateCertification,
                                 'project': CandidateProject,
                                 'reference': CandidateReference,
                                 'social-link': CandidateSocialLink,
                                 'language': CandidateLanguage,
                                 'achievement': CandidateAchievement}

    def get_serializer_class(self, entity_slug):
        return self.entity_slug_serializer_mapping.get(entity_slug)

    def get_model_class(self, entity_slug):
        return self.entity_slug_model_mapping.get(entity_slug)

    def post(self, request, *args, **kwargs):
        entity_slug = kwargs.get('entity_slug')
        data = request.data
        serializer_class = self.get_serializer_class(entity_slug)
        model_class = self.get_model_class(entity_slug)

        if not serializer_class:
            return Response({"detail": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

        invalid_data = False
        serializer_objs_list = []

        if not isinstance(data, list):
            return Response({"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

        total_records_received = len(data)

        for rcount, record in enumerate(data):
            obj_id = str(record.get('id', 0))

            if obj_id and not obj_id.isdigit():
                invalid_data = True
                break
            obj_id = int(obj_id)

            instance = model_class.objects.filter(id=obj_id).first()

            if not instance and obj_id != 0:
                invalid_data = True
                break

            if instance and instance.candidate.candidate_id != request.user.id:
                invalid_data = True
                break

            context = {'request': request}
            if instance:
                instance.initiate_image_upload_task = False

            if instance and rcount == (total_records_received - 1):
                instance.initiate_image_upload_task = True

            serializer_obj = serializer_class(data=record, instance=instance, context=context) if \
                instance else serializer_class(data=record, context=context)

            if not serializer_obj.is_valid():
                logging.getLogger('info_log').info(serializer_obj.errors)
                invalid_data = True
                break

            serializer_objs_list.append(serializer_obj)

        if invalid_data:
            return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        for obj in serializer_objs_list:
            obj.save()

        return Response([x.data for x in serializer_objs_list], status=status.HTTP_200_OK)


class CandidateShineProfileRetrieveUpdateView(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # candidate_email = request.session.get('email', '')
        candidate_email = 'amanpreet1040@gmail.com'
        if not candidate_email:
            return Response({}, status=400)

        shine_profile = ShineCandidateDetail().get_candidate_detail(email=candidate_email)

        if not shine_profile:
            return Response({})

        profile = shine_profile and shine_profile['personal_detail'][0]

        # update candidate basic profile
        candidate_profile_keys = ['first_name', 'last_name', 'email', 'number', 'date_of_birth', 'location', 'gender',
                                  'candidate_id']
        candidate_profile_values = [profile['first_name'], profile['last_name'], profile['email'],
                                    profile['cell_phone'], profile['date_of_birth'],
                                    profile['candidate_location'], profile['gender'], profile['id']]
        candidate_profile = dict(zip(candidate_profile_keys, candidate_profile_values))

        candidate = Candidate.objects.get_or_create(candidate_id=candidate_profile['candidate_id'],
                                                    defaults=candidate_profile)

        if candidate[1]:
            candidate.save()

        # # update candidate experience
        candidate_experience_keys = ['job_profile', 'company_name', 'start_date', 'end_date', 'is_working',
                                     'job_location',
                                     'work_description']
        experience = shine_profile and shine_profile['jobs']

        candidate_experience = []

        for exp in experience:
            start_date = datetime.strptime(exp['start_date'], '%Y-%m-%dT%H:%M:%S').date() \
                if exp['start_date'] is not None else \
                exp['start_date']
            end_date = datetime.strptime(exp['end_date'], '%Y-%m-%dT%H:%M:%S').date() \
                if exp['end_date'] is not None else \
                exp['end_date']
            candidate_experience_values = [exp['job_title'], exp['company_name'],
                                           start_date, end_date,
                                           exp['is_current'], '', exp['description']]
            experience_dict = dict(zip(candidate_experience_keys, candidate_experience_values))
            candidate_experience.append(CandidateExperience(**experience_dict))
            request.session['candidate_experience'] = candidate_experience

        return Response({
            "candidate_id": candidate_profile['candidate_id']
        })


class InterestView(ListAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        search_text = request.GET.get('search', '')
        return Response(
            {"data": dict([i for i in INTEREST_LIST if search_text.lower() in i[1].lower()])})


class OrderCustomisationListView(ListAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderCustomisationSerializer

    def get_queryset(self):
        return OrderCustomisation.objects.filter(candidate__candidate_id=self.candidate_id)

    def patch(self, request, *args, **kwargs):
        c_id = kwargs.get('candidate_id', '')
        candidate = Candidate.objects.filter(candidate_id=c_id).first()
        self.candidate_id = getattr(candidate, 'candidate_id','')
        if not self.candidate_id:
            return Response({"detail": "Candidate with given  candidate id is invalid."}, status= status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)


class OrderCustomisationRUDView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderCustomisationSerializer
    lookup_field = "template_no"
    lookup_url_kwarg = "template_no"

    def get_queryset(self):
        return OrderCustomisation.objects.filter(candidate__candidate_id=self.candidate_id)

    def patch(self, request, *args, **kwargs):
        c_id = kwargs.get('candidate_id', '')
        candidate = Candidate.objects.filter(candidate_id=c_id).first()
        self.candidate_id = getattr(candidate, 'candidate_id','')
        if not self.candidate_id:
            return Response({"detail": "Candidate with given  candidate id is invalid."}, status= status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        c_id = kwargs.get('candidate_id', '')
        candidate = Candidate.objects.filter(candidate_id=c_id).first()
        self.candidate_id = getattr(candidate, 'candidate_id','')
        if not self.candidate_id:
            return Response({"detail": "Candidate with given candidate id is invalid."}, status= status.HTTP_400_BAD_REQUEST)
        return super().get(request, *args, **kwargs)



class EntityReorderView(APIView):
    """
    Sample Input Data - 
    {
        "entity_id":5,
        "step":-1
    }
    """
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        candidate_id = kwargs.get('candidate_id')
        template_no = int(str(kwargs.get('template_no', '')))
        entity_id = str(request.data.get('entity_id', ''))
        step = str(request.data.get('step', ''))

        if not step or not step in ['1', '-1', '0']:
            return Response({"detail": "Please provide proper data"}, status=status.HTTP_400_BAD_REQUEST)

        entity_order_object = OrderCustomisation.objects.filter( \
            candidate__candidate_id=candidate_id, template_no=template_no).first()

        if not entity_order_object:
            return Response({"detail": "User data not found"}, status=status.HTTP_400_BAD_REQUEST)

        step = int(step)
        entity_id = int(entity_id)
        order_reshuffle_object = ResumeEntityReorderUtility(candidate_id=candidate_id, template_no=template_no)
        entity_position = order_reshuffle_object.move_entity(entity_id, step)
        entity_order_object.entity_position = json.dumps(entity_position)
        entity_order_object.save()

        return Response({"data": entity_order_object.entity_position}, status=status.HTTP_200_OK)


class ResumeImagePreviewView(APIView):
    """
    Returns base64 encoded image from cloud.
    If not found, returns 404.

    GET params supported - 

    quality - Image quality (0-100)
    """
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def get_image_base_64_encoded_data(self, candidate, template_no):

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
        options = {'quiet': '',
                   'quality': self.request and self.request.GET.get('quality', 40),
                   'format': 'JPG',
                   'disable-smart-width': '',
                   }

        file_obj = imgkit.from_string(rendered_template, False, options=options)
        return Response(base64.b64encode(file_obj))

    def get(self, request, *args, **kwargs):
        candidate_id = kwargs.get('candidate_id')
        template_no = kwargs.get('template_no')
        tsize = request.GET.get('tsize', '')

        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id).first()
        if not candidate_obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # if candidate_obj.candidate_id != request.user.id:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        name_suffix = template_no
        split_tsize = tsize.split("x")
        if tsize and len(split_tsize) > 1:
            name_suffix += "-{}x{}".format(split_tsize[0], split_tsize[1])

        if not settings.IS_GCP:
            try:
                file_obj = open("{}/{}/{}/images/resumetemplate-{}.jpg". \
                                format(settings.MEDIA_ROOT, settings.RESUME_TEMPLATE_DIR, candidate_obj.id,
                                       name_suffix), "rb")
            except Exception as e:
                logging.getLogger('error_log').error("Not Found - {}/{}/{}/images/resumetemplate-{}.jpg". \
                                                     format(settings.MEDIA_ROOT, settings.RESUME_TEMPLATE_DIR,
                                                            candidate_obj.id, template_no))
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            try:
                file_obj = GCPResumeBuilderStorage().open("{}/{}/images/resumetemplate-{}.jpg". \
                                                          format(settings.RESUME_TEMPLATE_DIR, candidate_obj.id,
                                                                 name_suffix), "rb")
            except Exception as e:
                logging.getLogger('error_log').error("Not Found - {}/{}/images/resumetemplate-{}.jpg". \
                                                     format(settings.RESUME_TEMPLATE_DIR, candidate_obj.id,
                                                            template_no))
                return Response(status=status.HTTP_404_NOT_FOUND)

        if not file_obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(base64.b64encode(file_obj.read()))


class SuggestionApiView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    PARAMS_MAPPING_TO_FUNCTION = {
        'autocomplete': {
            'job_title': 'get_job_title_suggestion'
        },
        'suggestion_job_title': {
            'experience': 'job_title_to_experience',
            'summary': 'job_title_to_summary'

        }
    }

    def get(self, request, *args, **kwargs):
        main_type = request.GET.get('main_type', None)
        if main_type:
            sub_type = request.GET.get('sub_type', None)
            if sub_type:
                func = self.PARAMS_MAPPING_TO_FUNCTION['suggestion_' + main_type].get(sub_type, None)
            else:
                func = self.PARAMS_MAPPING_TO_FUNCTION['autocomplete'].get(main_type, None)
            if func:
                return getattr(self, func)(request, *args, **kwargs)

        return Response(
            data=[],
            status=status.HTTP_200_OK
        )


    def set_suggestion_list(self,key, connection):
        # imports 
        from django_redis import get_redis_connection
        import os, sys
        ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
        ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
        ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

        if ROOT_FOLDER not in sys.path:
            sys.path.insert(1, ROOT_FOLDER + '/')
        if not connection: 
            conn = get_redis_connection('search_lookup')
        else: 
            conn = connection 


        if key == 'summary': 

            file_name = os.path.join(ROOT_FOLDER, 'merged_summary.json')
            # set summary in the redis
            with open(file_name) as fp:
                data = eval(fp.read())

            conn.hmset('suggestion_set_jt_summary', data)

        else : 
            file_name = os.path.join(ROOT_FOLDER, 'merged_experience.json')
            # set experience in the redis
            with open(file_name) as fp:
                data = eval(fp.read())

            conn.hmset('suggestion_set_jt_experience', data)



    def job_title_to_experience(self, request, *args, **kwargs):

        job_title = request.GET.get('query', None)
        cache = get_redis_connection('search_lookup')
        suggestion = []
        if cache.hlen('suggestion_set_jt_experience') == 0:
            self.set_suggestion_list('experience',cache)
        if job_title:
            job_title = job_title.title()
            suggest = cache.hget('suggestion_set_jt_experience', job_title.title())
            if suggest:
                suggestion = eval(suggest)

        return Response(
            data={'result': suggestion},
            status=status.HTTP_200_OK
        )

    def get_job_title_suggestion(self, request, *args, **kwargs):
        job_title = request.GET.get('query', None)
        if job_title:
            job_title = job_title.title()
            suggestion_keys = [key for key in JOB_TITLES if key.startswith(job_title)]
        return Response(
            data={'result': suggestion_keys},
            status=status.HTTP_200_OK
        )

    def job_title_to_summary(self, request, *args, **kwargs):
        job_title = request.GET.get('query', None)
        cache = get_redis_connection('search_lookup')
        suggestion = []
        if cache.hlen('suggestion_set_jt_summary') == 0:
            self.set_suggestion_list('summary', cache)

        if job_title:
            job_title = job_title.title()
            suggest = cache.hget('suggestion_set_jt_summary', job_title.title())
            if suggest:
                suggestion = eval(suggest)

        return Response(
            data={'result': suggestion},
            status=status.HTTP_200_OK
        )

class SessionAvailabilityAPIView(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        if (request.user and request.user.is_authenticated):
            try:
                candidate_id = request._request.session.get('candidate_id', '')
            except:
                candidate_id = ''
            return Response(
                data={
                    'result': True,
                    'candidate_id': candidate_id
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                'result': False,
                'candidate_id': ''
            },
            status=status.HTTP_200_OK 
        )


class PDFRefreshAPIView(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        from order.models import Order
        from order.tasks import generate_resume_for_order

        order_id = kwargs.get('order_id')
        # candidate_id = request.user.id
        c_id = kwargs.get('candidate_id', '')
        candidate = Candidate.objects.filter(candidate_id=c_id).first()
        candidate_id = getattr(candidate, 'candidate_id','')

        if not candidate_id:
            return Response({"detail": "Candidate with given  candidate id is invalid."}, status= status.HTTP_400_BAD_REQUEST)

        product_found = False
        order_obj_list = Order.objects.filter(id=order_id, candidate_id=candidate_id, status__in=[1, 3])

        if not order_obj_list:
            return Response({"detail": "Invalid Order id"}, status=status.HTTP_400_BAD_REQUEST)

        for order_obj in order_obj_list:
            if product_found:
                break

            for item in order_obj.orderitems.all():
                if item.product and item.product.type_flow == 17 and item.product.type_product == 0:
                    product_found = True
                    break

        if not product_found:
            return Response({"detail": "Invalid Order id"}, status=status.HTTP_400_BAD_REQUEST)
       
        # check wheter resume being sold by expert assistance and now generated by writer or user after selling it. 
        
        candidate_obj = Candidate.objects.filter(candidate_id = candidate_id).first()
        if not candidate_obj:
            return Response({"detail": "Candidate with given  candidate id is invalid."}, status= status.HTTP_400_BAD_REQUEST)
        candidate_obj.resume_generated = True 
        candidate_obj.save();
        generate_resume_for_order.delay(order_obj.id)
        return Response({"detail": "Resume successfully Updated"}, status=status.HTTP_200_OK)

class FreeTrialResumeDownload(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    '''
    use of the view is to download free trial resume of users with following functions
    1. post request to generate and send pdf file in response
    '''
    def post(self, request, *args, **kwargs):
        from resumebuilder.tasks import generate_and_upload_resume_pdf
        data = {
          'candidate_id': kwargs.get('candidate_id',''),
          'is_free_trial':True,
          'template_no': kwargs.get('template_no',1)
        }
        data = json.dumps(data)
        generate_and_upload_resume_pdf.delay(data)
        response = HttpResponse(json.dumps({'result':'Free Resume template creation started.Please wait for a few seconds'}))
        return response 

    def get(self,request,*args,**kwargs):
        candidate_id = kwargs.get('candidate_id','')
        template_no = kwargs.get('template_no','')
        candidate = Candidate.objects.filter(candidate_id=candidate_id).first()

        if not candidate:
            logging.getLogger('error_log').error("No Candidate Found")
            return HttpResponse(json.dumps({'error':True}))

        content_type = "application/pdf"
        filename_prefix = "free-trial"
        file_path = settings.RESUME_TEMPLATE_DIR + "/{}/pdf/free-trial-{}.pdf".format(candidate.id, template_no)
        content_type = "application/pdf"
        filename_suffix = ".pdf"

        try:
            if not settings.IS_GCP:
                file_path = "{}/{}".format(settings.MEDIA_ROOT, file_path)
                fsock = FileWrapper(open(file_path, 'rb'))
            else:
                fsock = GCPResumeBuilderStorage().open(file_path)

            filename = filename_prefix + filename_suffix
            response = HttpResponse(fsock.read(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response

        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
            return HttpResponse(json.dumps({'error':True}))



