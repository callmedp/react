from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer,
)
from rest_framework import serializers

from shared.rest_addons.mixins import SerializerFieldsMixin
from shop.models import Category, SubHeaderCategory
from shop.models import (
    Category, Product)
from cms.models import IndexColumn
from homepage.models import Testimonial

from homepage.models import Testimonial

class LoadMoreSerializerSolr(SerializerFieldsMixin,Serializer):
    id = serializers.CharField()
    django_ct = serializers.CharField()
    django_id = serializers.CharField()
    text = serializers.CharField()
    pHd= serializers.CharField()
    pFA = serializers.ListField(
        child=serializers.CharField())
    pFA_exact = serializers.ListField(
        child=serializers.CharField())
    pFAn = serializers.ListField(
        child=serializers.CharField())
    pCtg = serializers.ListField(
        child=serializers.CharField())
    pCC = serializers.CharField()
    pAb = serializers.CharField()
    pURL = serializers.CharField()
    pTt = serializers.CharField()
    pMtD = serializers.CharField()
    pNm = serializers.CharField()
    pSg = serializers.CharField()
    pTP = serializers.IntegerField()
    pTF = serializers.IntegerField()
    pUPC = serializers.CharField()
    pPc = serializers.CharField()
    pPv = serializers.IntegerField()
    pPvn = serializers.CharField()
    pCts = serializers.ListField(
        child=serializers.CharField())
    pAR = serializers.CharField()
    pAR_exact = serializers.CharField()
    pStM = serializers.ListField(
        child=serializers.CharField())
    pStM_exact = serializers.ListField(
        child=serializers.CharField())
    pDM = serializers.ListField(
        child=serializers.CharField())
    pDM_exact = serializers.ListField(
        child=serializers.CharField())
    pCert = serializers.ListField(
        child=serializers.CharField())
    pCert_exact = serializers.ListField(
        child=serializers.CharField())
    pAttrINR = serializers.ListField(
        child=serializers.CharField())
    pAttrUSD = serializers.ListField(
        child=serializers.CharField())
    pAttrAED = serializers.ListField(
        child=serializers.CharField())
    pAttrGBP = serializers.ListField(
        child=serializers.CharField())  
    pIc  = serializers.CharField()
    pIBg = serializers.IntegerField()
    pImg = serializers.CharField()
    pImA = serializers.CharField()
    pvurl = serializers.CharField()
    pDsc = serializers.CharField()
    pBS = serializers.CharField()
    pStar = serializers.ListField(
        child=serializers.CharField())
    pRC = serializers.IntegerField()
    pBC = serializers.IntegerField()
    pNJ = serializers.IntegerField()
    pVi = serializers.CharField()
    pViA = serializers.CharField()
    pVid = serializers.IntegerField()
    pVid_exact =  serializers.IntegerField()
    pCT  = serializers.CharField()
    pDD = serializers.IntegerField()
    pRD = serializers.BooleanField()
    pPinr = serializers.ListField(
        child=serializers.CharField())
    pPinr_exact = serializers.ListField(
        child=serializers.CharField())
    pPusd = serializers.ListField(
        child=serializers.CharField())
    pPusd_exact = serializers.ListField(
        child=serializers.CharField())
    pPaed = serializers.ListField(
        child=serializers.CharField())
    pPaed_exact = serializers.ListField(
        child=serializers.CharField())
    pPgbp = serializers.ListField(
        child=serializers.CharField())
    pPgbp_exact = serializers.ListField(
        child=serializers.CharField())
    pPin = serializers.FloatField()
    pPfin = serializers.FloatField()
    pPus = serializers.FloatField()
    pPfus = serializers.FloatField()
    pPae = serializers.FloatField()
    pPfae = serializers.FloatField()
    pPfgb = serializers.FloatField()
    pPinb = serializers.FloatField()
    pPfinb = serializers.FloatField()
    pPusb = serializers.FloatField() 
    pPfusb = serializers.FloatField()
    pPaeb = serializers.FloatField()
    pPfaeb = serializers.FloatField()
    pPgbb = serializers.FloatField()
    pPfgbb = serializers.FloatField()
    pAbx = serializers.CharField()
    pARx = serializers.CharField()
    pFAQs = serializers.CharField()
    pPChs = serializers.CharField()
    pCmbs = serializers.CharField()
    pVrs = serializers.CharField()
    pFBT = serializers.CharField()
    pCD = serializers.CharField()
    pMD = serializers.CharField()
    pSkill = serializers.ListField(
        child=serializers.CharField())
    pSkilln = serializers.ListField(
        child=serializers.CharField())
    pCtgsD = serializers.CharField()
    _version_ = serializers.IntegerField()
    pPOP = serializers.CharField()
    pAsft = serializers.JSONField()
    name = serializers.CharField(source="pNm")
    discount = SerializerMethodField()
    pTg = serializers.IntegerField()

    def get_discount(self, obj):
        if obj.pPfin != 0:
            return round((obj.pPfin-obj.pPin)*100/obj.pPfin,2)
        return 0

class SubHeaderCategorySerializer(ModelSerializer):
    class Meta:
        model = SubHeaderCategory
        exclude = ("created","modified","active","display_order","heading_choices","category",)

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ("created",)
    
class IndexColumnSerializer(ModelSerializer):
    class Meta:
        model = IndexColumn
        fields = ("url","name",)

class TestimonialSerializer(ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ("user_name","company", "designation", "review")
    
    def to_representation(self, instance):
        data = super(TestimonialSerializer, self).to_representation(instance)
        data['firstName'],data['lastName'] = data['user_name'].split(' ',1)
        data.pop('user_name')
        return data