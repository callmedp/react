from rest_framework import serializers
from homepage.models import TermAndAgreement

class TermsAndAgreementSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermAndAgreement
        fields = ['page_id','content']