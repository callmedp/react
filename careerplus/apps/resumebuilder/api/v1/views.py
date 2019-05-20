# python imports
from datetime import datetime, date

# django imports
from django.template.loader import get_template

# local imports
from resumebuilder.models import (Candidate, Skill, CandidateExperience, CandidateEducation, CandidateCertification,
                                  CandidateProject, CandidateReference, CandidateSocialLink, CandidateAchievement,
                                  CandidateLanguage)
from resumebuilder.api.core.serializers import (CandidateSerializer, SkillSerializer, CandidateExperienceSerializer,
                                                CandidateEducationSerializer, CandidateCertificationSerializer,
                                                CandidateProjectSerializer, CandidateAchievementSerializer,
                                                CandidateReferenceSerializer, CandidateSocialLinkSerializer,
                                                CandidateLanguageSerializer)

from resumebuilder.mixins import (SessionManagerMixin)
from resumebuilder.constants import EDUCATION_PARENT_CHILD_HEIRARCHY_LIST

# inter app imports
from shine.core import ShineCandidateDetail
from shared.rest_addons.authentication import ShineUserAuthentication
from shared.permissions import IsObjectOwner

# third party imports
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.views import (APIView)
from rest_framework.parsers import (FormParser, MultiPartParser)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from weasyprint import HTML, CSS


class CandidateListCreateView(ListCreateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateListCreateView, self).get_serializer(*args, **kwargs)


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
        return Skill.objects.filter(candidate=candidate_obj).order_by('order')

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
        return CandidateExperience.objects.filter(candidate=candidate_obj).order_by('order')

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
        return CandidateEducation.objects.filter(candidate=candidate_obj)

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
        return CandidateCertification.objects.filter(candidate=candidate_obj).order_by('order')

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
        return CandidateProject.objects.filter(candidate=candidate_obj).order_by('order')


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
        return CandidateReference.objects.filter(candidate=candidate_obj).order_by('order')


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
        return CandidateSocialLink.objects.filter(candidate=candidate_obj).order_by('order')


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
        return CandidateAchievement.objects.filter(candidate=candidate_obj).order_by('order')


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
        return CandidateLanguage.objects.filter(candidate=candidate_obj).order_by('order')

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

        template = get_template('resume{}_preview.html'.format(template_id))
        rendered_template = template.render(
            {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
             'achievements': achievements, 'references': references, 'projects': projects,
             'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
             'current_exp': current_exp, 'latest_exp': latest_experience,
             'preference_list': entity_preference,
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

        for record in data:
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
            serializer_obj = serializer_class(data=record, instance=instance, context=context) if \
                instance else serializer_class(data=record, context=context)

            if not serializer_obj.is_valid():
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

        #
        # request.session['candidate_id'] = candidate_profile['candidate_id']
        #
        # request.session['personal_info'] = candidate_profile

        #
        # # update candidate education
        # candidate_education_keys = ['candidate', 'specialization', 'institution_name', 'course_type', 'percentage_cgpa',
        #                        'start_date',
        #                        'end_date', 'is_pursuing']
        # education = shine_profile and shine_profile['education']
        # candidate_education = []
        # for edu in education:
        #     course_type = ""
        #     if edu['course_type'] == 1:
        #         course_type = "FT"
        #     elif edu['course_type'] == 2:
        #         course_type = "PT"
        #     else:
        #         course_type = "CR"
        #
        #     degree_index = next((index for (index, d) in enumerate(educ_list) if d["pid"] == edu['education_level']),
        #                         None)
        #
        #     degree_name = educ_list[degree_index]['pdesc'];
        #
        #     child = educ_list[degree_index]['child']
        #
        #     specialization_index = next((index for (index, d) in enumerate(child)
        #                                  if d['cid'] == edu['education_specialization']), None)
        #     specialization_name = child[specialization_index]['cdesc']
        #
        #     candidate_education_values = [candidate, '{}({})'.format(degree_name, specialization_name), edu['institute_name'],
        #                              course_type,
        #                              '',
        #                              None, None, True]
        #     education_dict = dict(zip(candidate_education_keys, candidate_education_values))
        #     candidate_education.append(CandidateEducation(**education_dict))
        #
        # # bulk candidate eudcation create
        # CandidateEducation.objects.bulk_create(candidate_education)
        #
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
        #
        # CandidateExperience.objects.bulk_create(candidate_experience)
        #
        # # update candidate skills
        # skill_keys = ['candidate', 'name', 'proficiency']
        # skills = shine_profile and shine_profile['skills']
        #
        # candidate_skill = []
        #
        # for skill in skills:
        #     candidate_skill_values = [candidate, skill['value'], 5]
        #     skill_dict = dict(zip(skill_keys, candidate_skill_values))
        #     candidate_skill.append(Skill(**skill_dict))
        #
        # Skill.objects.bulk_create(candidate_skill)
        #
        # # update candidate languages
        # candidate_language = []
        #
        # # update candidate achievements
        #
        # # update candidate certification
        # candidate_certification_keys = ['candidate', 'name_of_certification', 'year_of_certification']
        # certifications = shine_profile and shine_profile['certifications']
        # candidate_certification = []
        #
        # for certi in certifications:
        #     candidate_certificaiton_values = [candidate, certi['certification_name'], certi['certification_year']]
        #     certification_dict = dict(zip(candidate_certification_keys, candidate_certificaiton_values))
        #     candidate_certification.append(CandidateCertification(**certification_dict))
        #
        # CandidateCertification.objects.bulk_create(candidate_certification)
        #
        # # update candidate social links
        # candidate_social_links = []
        #
        # # update candidate reference
        # candidate_references = []
        #
        # # update candidate projects
        # candidate_projects = []

        return Response({
            "candidate_id": candidate_profile['candidate_id']
        })
