from rest_framework.generics import ListAPIView
from .serializers import TermsAndAgreementSerializer
from homepage.models import TermAndAgreement

class TermsAndAgreementView(ListAPIView):
    # queryset = TermAndAgreement.objects.all()
    serializer_class = TermsAndAgreementSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        page_id = self.request.query_params.get('page_id','')
        if page_id:
            return TermAndAgreement.objects.filter(page_id=page_id)
        return TermAndAgreement.objects.all()