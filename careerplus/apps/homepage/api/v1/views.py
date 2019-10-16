from rest_framework.generics import RetrieveAPIView
from .serializers import StaticSiteContentSerializer
from homepage.models import StaticSiteContent

class StaticSiteView(RetrieveAPIView):
    # queryset = TermAndAgreement.objects.all()
    serializer_class = StaticSiteContentSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        page_type = int(self.kwargs['pk'])
        if page_type:
            return StaticSiteContent.objects.filter(page_type=page_type)
        return StaticSiteContent.objects.all()