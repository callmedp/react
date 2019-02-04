# python imports

# django imports

# local imports
from resumebuilder.models import (Skill, )
from resumebuilder.api.core.skill_serializer import (SkillSerializer)

# inter app imports

# third party imports
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView, )


class SkillListCreateApiView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(SkillListCreateApiView, self).get_serializer(*args, **kwargs)


class SkillRetrieveUpdateApiView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = SkillSerializer

    def get_queryset(self):
        skill_id = int(self.kwargs.get('pk'))
        return Skill.objects.filter(id=skill_id)
