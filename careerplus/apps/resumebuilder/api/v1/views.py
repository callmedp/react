# python imports
from datetime import datetime

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

# inter app imports
from shine.core import ShineCandidateDetail
from .education_specialization import educ_list
from shared.rest_addons.authentication import ShineUserAuthentication
from shared.permissions import IsObjectOwner

# third party imports
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.views import (APIView)
from rest_framework.parsers import (FormParser, MultiPartParser)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class CandidateListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateListCreateView, self).get_serializer(*args, **kwargs)


class CandidateRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    lookup_field = 'candidate_id'
    lookup_url_kwarg = 'pk'
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    owner_fields = ['candidate_id']

    # def get(self, request, *args, **kwargs):
    #     import ipdb;
    #     ipdb.set_trace();
    #     if 'personal_info' not in self.request.session:
    #         candidate_id = self.kwargs.get('pk')
    #         candidate = Candidate.objects.filter(candidate_id=candidate_id).values().first()
    #         return Response(candidate)
    #
    #     else:
    #         personal_info = self.request.session.get('personal_info')
    #         del request.session['personal_info']
    #         candidate = Candidate.objects.get_or_create(candidate_id=personal_info['candidate_id'],
    #                                                     defaults=personal_info)
    #         if candidate[1]:
    #             candidate.save()
    #         return Response(personal_info)


class SkillListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(SkillListCreateView, self).get_serializer(*args, **kwargs)


class SkillRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsObjectOwner,)
    serializer_class = SkillSerializer

    owner_fields = ['candidate_id']

    def get_queryset(self):
        skill_id = int(self.kwargs.get('pk'))
        return Skill.objects.filter(id=skill_id)


class CandidateShineProfileRetrieveUpdateView(APIView):
    authentication_classes = ()
    permission_classes = ()

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


class CandidateExperienceListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateExperience.objects.all()
    serializer_class = CandidateExperienceSerializer

    # def get_queryset(self):
    #     candidate_id = self.request.GET.get('c_id', '')
    #     if 'candidate_experience' not in self.request.session:
    #         candidate = Candidate.objects.get(candidate_id=candidate_id)
    #         return candidate.candidateexperience_set.all()

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateExperienceListCreateView, self).get_serializer(*args, **kwargs)


class CandidateExperienceRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateExperience.objects.all()
    serializer_class = CandidateExperienceSerializer

    # def get_queryset(self):
    #     candidate_experience_id = int(self.kwargs.get('pk'))
    #     return CandidateExperience.objects.filter(id=candidate_experience_id)
    #


class CandidateEducationListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateEducation.objects.all()
    serializer_class = CandidateEducationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateEducationListCreateView, self).get_serializer(*args, **kwargs)


class CandidateEducationRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateEducationSerializer

    def get_queryset(self):
        candidate_education_id = int(self.kwargs.get('pk'))
        return CandidateEducation.objects.filter(id=candidate_education_id)


class CandidateCertificationListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateCertification.objects.all()
    serializer_class = CandidateCertificationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateCertificationListCreateView, self).get_serializer(*args, **kwargs)


class CandidateCertificationRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateCertificationSerializer

    def get_queryset(self):
        candidate_certification_id = int(self.kwargs.get('pk'))
        return CandidateCertification.objects.filter(id=candidate_certification_id)


class CandidateProjectListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateProject.objects.all()
    serializer_class = CandidateProjectSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateProjectListCreateView, self).get_serializer(*args, **kwargs)


class CandidateProjectRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateProjectSerializer

    def get_queryset(self):
        candidate_project_id = int(self.kwargs.get('pk'))
        return CandidateProject.objects.filter(id=candidate_project_id)


class CandidateReferenceListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateReference.objects.all()
    serializer_class = CandidateReferenceSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateReferenceListCreateView, self).get_serializer(*args, **kwargs)


class CandidateReferenceRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateReferenceSerializer

    def get_queryset(self):
        candidate_reference_id = int(self.kwargs.get('pk'))
        return CandidateReference.objects.filter(id=candidate_reference_id)


class CandidateSocialLinkListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateSocialLink.objects.all()
    serializer_class = CandidateSocialLinkSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateSocialLinkListCreateView, self).get_serializer(*args, **kwargs)


class CandidateSocialLinkRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateSocialLinkSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return CandidateSocialLink.objects.filter(id=external_link_id)


class CandidateAchievementListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateAchievement.objects.all()
    serializer_class = CandidateAchievementSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateAchievementListCreateView, self).get_serializer(*args, **kwargs)


class CandidateAchievementRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateAchievementSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return CandidateAchievement.objects.filter(id=external_link_id)


class CandidateLanguageListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = CandidateLanguage.objects.all()
    serializer_class = CandidateLanguageSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CandidateLanguageListCreateView, self).get_serializer(*args, **kwargs)


class CandidateLanguageRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = CandidateLanguageSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return CandidateLanguage.objects.filter(id=external_link_id)


class CandidateResumePreview(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        candidate_id = self.kwargs.get('candidate_id', '')
        template_id = self.kwargs.get('pk', '');

        candidate = Candidate.objects.filter(candidate_id=candidate_id).first()
        if not candidate:
            return {}

        # extracurricular = candidate.extracurricular.split(',')
        education = candidate.candidateeducation_set.all()
        experience = candidate.candidateexperience_set.all()
        skills = candidate.skill_set.all()
        achievements = candidate.candidateachievement_set.all()
        references = candidate.candidatereference_set.all()
        projects = candidate.candidateproject_set.all()
        certifications = candidate.candidatecertification_set.all()
        languages = candidate.candidatelanguage_set.all()
        current_exp = experience.filter(is_working=True).order_by('-start_date').first()

        template = get_template('resume{}.html'.format(template_id))
        rendered_template = template.render(
            {'candidate': candidate, 'education': education, 'experience': experience, 'skills': skills,
             'achievements': achievements, 'references': references, 'projects': projects,
             'certifications': certifications, 'extracurricular': '', 'languages': languages,
             'current_exp': current_exp}).encode(encoding='UTF-8')

        return Response({
            'html': rendered_template
        })
