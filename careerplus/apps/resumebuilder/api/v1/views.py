# python imports
from datetime import datetime
# django imports

# local imports
from resumebuilder.models import (User, Skill, UserExperience, UserEducation, UserCertification,
                                  UserProject, UserReference, UserSocialLink, UserAchievement)
from resumebuilder.api.core.serializers import (UserSerializer, SkillSerializer, UserExperienceSerializer,
                                                UserEducationSerializer, UserCertificationSerializer,
                                                UserProjectSerializer, UserAchievementSerializer,
                                                UserReferenceSerializer, UserSocialLinkSerializer)

from resumebuilder.mixins import (SessionManagerMixin)
# inter app imports
from shine.core import ShineCandidateDetail

from .education_specialization import educ_list
# third party imports
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, )
from rest_framework.parsers import (FormParser, MultiPartParser)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class UserListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserListCreateView, self).get_serializer(*args, **kwargs)


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()
    # parser_class = (FormParser, MultiPartParser)

    serializer_class = UserSerializer

    # def put(self, request, *args, **kwargs):
    #     user_id = int(kwargs.get('pk'))
    #     user = User.objects.filter(id=user_id)
    #     import ipdb
    #     ipdb.set_trace()

    #     update user with info provided.
    #     return updated_user

    def get_queryset(self):
        import ipdb;
        ipdb.set_trace();
        candidate_id = (self.kwargs.get('pk'))
        return User.objects.filter(candidate_id=candidate_id)


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
    authentication_classes = ()
    permission_classes = ()

    serializer_class = SkillSerializer

    def get_queryset(self):
        skill_id = int(self.kwargs.get('pk'))
        return Skill.objects.filter(id=skill_id)


class UserShineProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        user_email = kwargs.get('email')
        if not user_email:
            return Response({}, status=400)

        shine_profile = ShineCandidateDetail().get_candidate_detail(email=user_email)

        if not shine_profile:
            return Response({})

        profile = shine_profile and shine_profile['personal_detail'][0]

        # update user basic profile
        user_profile_keys = ['first_name', 'last_name', 'email', 'number', 'date_of_birth', 'location', 'gender',
                             'candidate_id']
        user_profile_values = [profile['first_name'], profile['last_name'], profile['email'],
                               profile['cell_phone'], profile['date_of_birth'],
                               profile['candidate_location'], profile['gender'], profile['id']]
        user_profile = dict(zip(user_profile_keys, user_profile_values))

        request.session['candidate_id'] = user_profile['candidate_id']

        request.session['personal_info'] = user_profile

        user = User.objects.get_or_create(email=user_profile['email'], defaults=user_profile)

        if user[1]:
            user.save()

        # user = user[0]
        #
        # # update user education
        # user_education_keys = ['user', 'specialization', 'institution_name', 'course_type', 'percentage_cgpa',
        #                        'start_date',
        #                        'end_date', 'is_pursuing']
        # education = shine_profile and shine_profile['education']
        # user_education = []
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
        #     user_education_values = [user, '{}({})'.format(degree_name, specialization_name), edu['institute_name'],
        #                              course_type,
        #                              '',
        #                              None, None, True]
        #     education_dict = dict(zip(user_education_keys, user_education_values))
        #     user_education.append(UserEducation(**education_dict))
        #
        # # bulk user eudcation create
        # UserEducation.objects.bulk_create(user_education)
        #
        # # update user experience
        # user_experience_keys = ['user', 'job_profile', 'company_name', 'start_date', 'end_date', 'is_working',
        #                         'job_location',
        #                         'work_description']
        # experience = shine_profile and shine_profile['jobs']
        #
        # user_experience = []
        #
        # for exp in experience:
        #     start_date = datetime.strptime(exp['start_date'], '%Y-%m-%dT%H:%M:%S').date() \
        #         if exp['start_date'] is not None else \
        #         exp['start_date']
        #     end_date = datetime.strptime(exp['end_date'], '%Y-%m-%dT%H:%M:%S').date() \
        #         if exp['end_date'] is not None else \
        #         exp['end_date']
        #     user_experience_values = [user, exp['job_title'], exp['company_name'],
        #                               start_date, end_date,
        #                               exp['is_current'], '', exp['description']]
        #     experience_dict = dict(zip(user_experience_keys, user_experience_values))
        #     user_experience.append(UserExperience(**experience_dict))
        #
        # UserExperience.objects.bulk_create(user_experience)
        #
        # # update user skills
        # skill_keys = ['user', 'name', 'proficiency']
        # skills = shine_profile and shine_profile['skills']
        #
        # user_skill = []
        #
        # for skill in skills:
        #     user_skill_values = [user, skill['value'], 5]
        #     skill_dict = dict(zip(skill_keys, user_skill_values))
        #     user_skill.append(Skill(**skill_dict))
        #
        # Skill.objects.bulk_create(user_skill)
        #
        # # update user languages
        # user_language = []
        #
        # # update user achievements
        #
        # # update user certification
        # user_certification_keys = ['user', 'name_of_certification', 'year_of_certification']
        # certifications = shine_profile and shine_profile['certifications']
        # user_certification = []
        #
        # for certi in certifications:
        #     user_certificaiton_values = [user, certi['certification_name'], certi['certification_year']]
        #     certification_dict = dict(zip(user_certification_keys, user_certificaiton_values))
        #     user_certification.append(UserCertification(**certification_dict))
        #
        # UserCertification.objects.bulk_create(user_certification)
        #
        # # update user social links
        # user_social_links = []
        #
        # # update user reference
        # user_references = []
        #
        # # update user projects
        # user_projects = []

        return Response({
            "candidate_id": user_profile['candidate_id']
        })


class UserExperienceListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserExperience.objects.all()
    serializer_class = UserExperienceSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserExperienceListCreateView, self).get_serializer(*args, **kwargs)


class UserExperienceRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserExperienceSerializer

    def get_queryset(self):
        user_experience_id = int(self.kwargs.get('pk'))
        return UserExperience.objects.filter(id=user_experience_id)


class UserEducationListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserEducationListCreateView, self).get_serializer(*args, **kwargs)


class UserEducationRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserEducationSerializer

    def get_queryset(self):
        user_education_id = int(self.kwargs.get('pk'))
        return UserEducation.objects.filter(id=user_education_id)


class UserCertificationListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserCertification.objects.all()
    serializer_class = UserCertificationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserCertificationListCreateView, self).get_serializer(*args, **kwargs)


class UserCertificationRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserCertificationSerializer

    def get_queryset(self):
        user_certification_id = int(self.kwargs.get('pk'))
        return UserCertification.objects.filter(id=user_certification_id)


class UserProjectListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserProjectListCreateView, self).get_serializer(*args, **kwargs)


class UserProjectRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserProjectSerializer

    def get_queryset(self):
        user_project_id = int(self.kwargs.get('pk'))
        return UserProject.objects.filter(id=user_project_id)


class UserReferenceListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserReference.objects.all()
    serializer_class = UserReferenceSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserReferenceListCreateView, self).get_serializer(*args, **kwargs)


class UserReferenceRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserReferenceSerializer

    def get_queryset(self):
        user_reference_id = int(self.kwargs.get('pk'))
        return UserReference.objects.filter(id=user_reference_id)


class UserSocialLinkListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserSocialLink.objects.all()
    serializer_class = UserSocialLinkSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserSocialLinkListCreateView, self).get_serializer(*args, **kwargs)


class UserSocialLinkRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserSocialLinkSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return UserSocialLink.objects.filter(id=external_link_id)


class UserAchievementListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserAchievementListCreateView, self).get_serializer(*args, **kwargs)


class UserAchievementRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserAchievementSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return UserAchievement.objects.filter(id=external_link_id)


class UserResumePreview(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'resume4.html'

    def get(self, request):
        user = User.objects.get(id=95)
        extracurricular = user.extracurricular.split(',')
        education = user.usereducation_set.all()
        experience = user.userexperience_set.all()
        skills = user.skill_set.all()
        achievements = user.userachievement_set.all()
        references = user.userreference_set.all()
        projects = user.userproject_set.all()
        certifications = user.usercertification_set.all()
        languages = user.userlanguage_set.all()
        current_exp = experience.filter(is_working=True).order_by('-start_date').first()

        return Response({'user': user, 'education': education, 'experience': experience, 'skills': skills,
                         'achievements': achievements, 'references': references, 'projects': projects,
                         'certifications': certifications, 'extracurricular': extracurricular, 'languages': languages,
                         'current_exp': current_exp})
