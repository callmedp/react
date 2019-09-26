from rest_framework.generics import ListAPIView
from .serializers import StaticSiteContentSerializer
from homepage.models import StaticSiteContent

class StaticSiteView(ListAPIView):
    # queryset = TermAndAgreement.objects.all()
    serializer_class = StaticSiteContentSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        page_type = self.request.query_params.get('page_type','')
        if page_type:
            return StaticSiteContent.objects.filter(page_type=page_type)
        return StaticSiteContent.objects.all()