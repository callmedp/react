from haystack import indexes
from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    pURL = indexes.CharField(model_attr='url')
    pTt = indexes.CharField(model_attr='title')
    pMtD = indexes.CharField(model_attr='meta_desc')
    pMK = indexes.CharField(model_attr='meta_keywords', default='')
    pHd = indexes.CharField(model_attr='heading')
    pNm = indexes.CharField(model_attr='name')
    pSg = indexes.CharField(model_attr='slug')
    pTS = indexes.IntegerField(model_attr='type_service', default=0)
    pTP = indexes.IntegerField(model_attr='type_product', default=0)
    pTF = indexes.IntegerField(model_attr='type_flow', default=0)
    pUPC = indexes.CharField(model_attr='upc')
    pBnr = indexes.CharField(model_attr='banner')
    pIc = indexes.CharField(model_attr='icon')
    pIBg = indexes.IntegerField(model_attr='image_bg', default=0)
    pImg = indexes.CharField(model_attr='image')
    pImA = indexes.CharField(model_attr='image_alt')
    pVd = indexes.CharField(model_attr='video_url')
    pFI = indexes.CharField(model_attr='flow_image')
    pEcc = indexes.CharField(model_attr='email_cc', default='')
    pAb = indexes.CharField(model_attr='about', default='')
    pDsc = indexes.CharField(model_attr='description', default='')
    pBS = indexes.CharField(model_attr='buy_shine', default='')
    pMDsc = indexes.CharField(model_attr='mail_desc', default='')
    pCDsc = indexes.CharField(model_attr='call_desc', default='')
    pDM = indexes.IntegerField(model_attr='duration_months', default=0, faceted=True)
    pDD = indexes.IntegerField(model_attr='duration_days', default=0)
    pEx = indexes.IntegerField(model_attr='experience', default=0)
    pRD = indexes.BooleanField(model_attr='requires_delivery', default=True)
    pCert = indexes.BooleanField(model_attr='certification', default=True, faceted=True)
    pSM = indexes.IntegerField(model_attr='study_mode', default=0, faceted=True)
    pCT = indexes.IntegerField(model_attr='course_type', default=0, faceted=True)
    pAR = indexes.DecimalField(model_attr='avg_rating', faceted=True)
    pRC = indexes.IntegerField(default=0, model_attr='no_review')
    pBC = indexes.IntegerField(default=0, model_attr='buy_count')
    pNJ = indexes.IntegerField(default=0, model_attr='num_jobs')
    pSK = indexes.CharField(default='', model_attr='search_keywords') 
    pCts = indexes.MultiValueField(model_attr='countries__name')
    pVtn = indexes.MultiValueField(model_attr='variation__name')
    pRtd = indexes.MultiValueField(model_attr='related__name')
    pCds = indexes.MultiValueField(model_attr='childs__name')
    pCtg = indexes.MultiValueField(model_attr='categories__name', faceted=True)
    pKwds = indexes.MultiValueField(model_attr='keywords__name')
    pVnd = indexes.CharField(model_attr='vendor__name')
    pChts = indexes.MultiValueField(model_attr='chapters__heading')
    pFqs = indexes.MultiValueField(model_attr='faqs__text')
    pAts = indexes.MultiValueField(model_attr='attributes__display_name')
    pPrs = indexes.MultiValueField(model_attr='prices__value', faceted=True)
    pIA = indexes.BooleanField(default=False, model_attr='active')

    def get_model(self):
        return Product
