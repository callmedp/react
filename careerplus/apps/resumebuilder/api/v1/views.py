# python imports

# django imports

# local imports
from resumebuilder.models import (User, Skill, UserExperience, UserEducation, UserCertification,
                                  UserProject, UserReference, ExternalLink, UserAchievement)
from resumebuilder.api.core.serializers import (UserSerializer, SkillSerializer, UserExperienceSerializer,
                                                UserEducationSerializer, UserCertificationSerializer,
                                                UserProjectSerializer, UserAchievementSerializer,
                                                UserReferenceSerializer, ExternalLinkSerializer)

from resumebuilder.mixins import (SessionManagerMixin)
# inter app imports

# third party imports
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, )
from rest_framework.parsers import (FormParser, MultiPartParser)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class UserListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserListCreateView, self).get_serializer(*args, **kwargs)


class UserRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()
    parser_class = (FormParser, MultiPartParser)

    serializer_class = UserSerializer

    # def put(self, request, *args, **kwargs):
    #     user_id = int(kwargs.get('pk'))
    #     user = User.objects.filter(id=user_id)
    #     import ipdb
    #     ipdb.set_trace()

    #     update user with info provided.
    #     return updated_user

    def get_queryset(self):
        user_id = int(self.kwargs.get('pk'))
        return User.objects.filter(id=user_id)


class SkillListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(SkillListCreateView, self).get_serializer(*args, **kwargs)


class SkillRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = SkillSerializer

    def get_queryset(self):
        skill_id = int(self.kwargs.get('pk'))
        return Skill.objects.filter(id=skill_id)


class UserExperienceListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserExperience.objects.all()
    serializer_class = UserExperienceSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserExperienceListCreateView, self).get_serializer(*args, **kwargs)


class UserExperienceRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserExperienceSerializer

    def get_queryset(self):
        user_experience_id = int(self.kwargs.get('pk'))
        return UserExperience.objects.filter(id=user_experience_id)


class UserEducationListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserEducationListCreateView, self).get_serializer(*args, **kwargs)


class UserEducationRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserEducationSerializer

    def get_queryset(self):
        user_education_id = int(self.kwargs.get('pk'))
        return UserEducation.objects.filter(id=user_education_id)


class UserCertificationListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserCertification.objects.all()
    serializer_class = UserCertificationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserCertificationListCreateView, self).get_serializer(*args, **kwargs)


class UserCertificationRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserCertificationSerializer

    def get_queryset(self):
        user_certification_id = int(self.kwargs.get('pk'))
        return UserCertification.objects.filter(id=user_certification_id)


class UserProjectListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserProjectListCreateView, self).get_serializer(*args, **kwargs)


class UserProjectRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserProjectSerializer

    def get_queryset(self):
        user_project_id = int(self.kwargs.get('pk'))
        return UserProject.objects.filter(id=user_project_id)


class UserReferenceListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserReference.objects.all()
    serializer_class = UserReferenceSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserReferenceListCreateView, self).get_serializer(*args, **kwargs)


class UserReferenceRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserReferenceSerializer

    def get_queryset(self):
        user_reference_id = int(self.kwargs.get('pk'))
        return UserReference.objects.filter(id=user_reference_id)


class ExternalLinkListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ExternalLink.objects.all()
    serializer_class = ExternalLinkSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(ExternalLinkListCreateView, self).get_serializer(*args, **kwargs)


class ExternalLinkRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = ExternalLinkSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return ExternalLink.objects.filter(id=external_link_id)


class UserAchievementListCreateView(SessionManagerMixin, ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserAchievementListCreateView, self).get_serializer(*args, **kwargs)


class UserAchievementRetrieveUpdateView(SessionManagerMixin, RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserAchievementSerializer

    def get_queryset(self):
        external_link_id = int(self.kwargs.get('pk'))
        return UserAchievement.objects.filter(id=external_link_id)


class UserResumePreview(SessionManagerMixin, RetrieveUpdateAPIView):
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

        return Response({'user': user, 'education': education, 'experience': experience, 'skills': skills,
                         'achievements': achievements, 'references': references, 'projects': projects,
                         'certifications': certifications, 'extracurricular': extracurricular})
