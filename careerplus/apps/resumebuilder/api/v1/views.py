# python imports

# django imports

# local imports
from resumebuilder.models import (User, Skill, UserExperience, UserEducation, UserCertification,
                                  UserProject, UserReference, ExternalLink)
from resumebuilder.api.core.serializers import (UserSerializer, SkillSerializer, UserExperienceSerializer,
                                                UserEducationSerializer, UserCertificationSerializer,
                                                UserProjectSerializer, UserReferenceSerializer, ExternalLinkSerializer)

from resumebuilder.mixins import (SessionManagerMixin)
# inter app imports

# third party imports
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, )


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

    serializer_class = UserSerializer

    # def put(self, request, *args, **kwargs):
    #     user_id = int(kwargs.get('pk'))
    #     user = User.objects.filter(id=user_id)
    #     import ipdb;
    #     ipdb.set_trace();
    #     info = request.data
    # #     update user with info provided.
    # #     return updated_user


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
