from haystack import indexes
from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True, use_template=True,
        template_name='search/indexes/shop/product_text.txt')
    id = indexes.IntegerField(model_attr='id')
    # Meta and SEO #
    pURL = indexes.CharField(null=True, indexed=False)
    pTt = indexes.CharField(model_attr='title', null=True, indexed=False)
    pMtD = indexes.CharField(model_attr='meta_desc', null=True, indexed=False)
    pMK = indexes.CharField(model_attr='meta_keywords', null=True, indexed=False)
    pHd = indexes.EdgeNGramField(model_attr='heading', null=True)
    pHdx = indexes.CharField(model_attr='heading', null=True, indexed=False)
    
    # Control Field #
    pNm = indexes.CharField(model_attr='name', null=True)
    pSg = indexes.CharField(model_attr='slug', null=True)
    pTP = indexes.IntegerField(model_attr='type_product', default=0)
    pTF = indexes.IntegerField(model_attr='type_flow', default=0)
    pUPC = indexes.CharField(model_attr='upc', null=True, indexed=False)
    
    # Content Field#
    pIc = indexes.CharField(model_attr='icon', indexed=False)
    pIBg = indexes.IntegerField(model_attr='image_bg', default=0, indexed=False)
    pImg = indexes.CharField(model_attr='image', indexed=False)
    pImA = indexes.CharField(model_attr='image_alt', null=True, indexed=False)
    pVd = indexes.CharField(model_attr='video_url', indexed=False)
    pAb = indexes.CharField(model_attr='about', default='')
    pDsc = indexes.CharField(model_attr='description', default='')
    pBS = indexes.CharField(model_attr='buy_shine', default='')
    
    #Facets Fields#
    pPc = indexes.CharField(null=True, faceted=True)
    pPv = indexes.CharField(null=True, faceted=True)
    pAR = indexes.DecimalField(model_attr='avg_rating', faceted=True)
    
    # pDM = indexes.IntegerField(model_attr='duration_months', default=0, faceted=True)
    # pDD = indexes.IntegerField(model_attr='duration_days', default=0)
    # pEx = indexes.IntegerField(model_attr='experience', default=0)
    # pRD = indexes.BooleanField(model_attr='requires_delivery', default=True)
    # pCert = indexes.BooleanField(model_attr='certification', default=True, faceted=True)
    # pSM = indexes.IntegerField(model_attr='study_mode', default=0, faceted=True)
    # pCT = indexes.IntegerField(model_attr='course_type', default=0, faceted=True)
    
    pRC = indexes.IntegerField(default=0, model_attr='no_review')
    pBC = indexes.IntegerField(default=0, model_attr='buy_count')
    pNJ = indexes.IntegerField(default=0, model_attr='num_jobs')
    pSK = indexes.CharField(default='') 
    
    # pCts = indexes.MultiValueField(model_attr='countries__name')
    # pVtn = indexes.MultiValueField(model_attr='variation__name')
    # pRtd = indexes.MultiValueField(model_attr='related__name')
    # pCds = indexes.MultiValueField(model_attr='childs__name')
    # pCtg = indexes.MultiValueField(model_attr='categories__name', faceted=True)
    # pKwds = indexes.MultiValueField(model_attr='keywords__name')
    # pVnd = indexes.CharField(model_attr='vendor__name')
    # pChts = indexes.MultiValueField(model_attr='chapters__heading')
    # pFqs = indexes.MultiValueField(model_attr='faqs__text')
    # pAts = indexes.MultiValueField(model_attr='attributes__display_name')
    # pPrs = indexes.MultiValueField(model_attr='prices__value', faceted=True)
    # pIA = indexes.BooleanField(default=False, model_attr='active')

    def get_model(self):
        return Product

    def prepare_pURL(self, obj):
        return obj.get_url()

    def prepare_pPc(self, obj):
        if obj.product_class:
            return obj.product_class.name
        return ''

    def prepare_pPv(self, obj):
        if obj.vendor:
            return obj.vendor.name
        return ''

    def prepare_pIc(self, obj):
        return obj.get_icon_url()
        
    def prepare_pImg(self, obj):
        return obj.get_image_url()

       