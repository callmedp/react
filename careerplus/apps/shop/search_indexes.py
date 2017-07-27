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
    pHd = indexes.EdgeNgramField(model_attr='heading', null=True)
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
    pvurl = indexes.CharField(model_attr='video_url', indexed=False)
    pAb = indexes.CharField(model_attr='about', default='')
    pDsc = indexes.CharField(model_attr='description', default='')
    pBS = indexes.CharField(model_attr='buy_shine', default='')
    
    #Facets & Attributes Fields#
    pPc = indexes.CharField(null=True, faceted=True)
    pPV = indexes.CharField(null=True, faceted=True)
    pAR = indexes.DecimalField(model_attr='avg_rating', faceted=True)
    pCtg = indexes.MultiValueField(null=True, faceted=True)
    pCts = indexes.MultiValueField(null=True)
    pFA = indexes.MultiValueField(null=True, faceted=True)
    pDM = indexes.IntegerField(default=0, faceted=True)
    pDD = indexes.IntegerField(default=0, faceted=True)
    pRD = indexes.BooleanField(default=True)
    pCert = indexes.BooleanField(default=False, faceted=True)
    pEX = indexes.CharField(null=True, faceted=True)
    pStM = indexes.CharField(null=True, faceted=True)
    pCT = indexes.CharField(null=True, faceted=True)
    
    pStar = indexes.CharField(null=True, indexed=False)
    pRC = indexes.IntegerField(default=0, model_attr='no_review', indexed=False)
    pBC = indexes.IntegerField(default=0, model_attr='buy_count', indexed=False)
    pNJ = indexes.IntegerField(default=0, model_attr='num_jobs', indexed=False)
    pVi = indexes.CharField(null=True, indexed=False)
    
    #Price Fields#
    pPinr = indexes.DecimalField(model_attr='inr_price', faceted=True)
    pPfinr = indexes.DecimalField(model_attr='fake_inr_price', faceted=True)
    pPusd = indexes.DecimalField(model_attr='usd_price', faceted=True)
    pPfusd = indexes.DecimalField(model_attr='fake_usd_price', faceted=True)
    pPaed = indexes.DecimalField(model_attr='aed_price', faceted=True)
    pPfaed = indexes.DecimalField(model_attr='fake_aed_price', faceted=True)
    pPgbp = indexes.DecimalField(model_attr='gbp_price', faceted=True)
    pPfgbp = indexes.DecimalField(model_attr='fake_gbp_price', faceted=True)
    
    
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

    def index_queryset(self, using=None):
        return self.get_model().indexable.all()

    def read_queryset(self, using=None):
        return self.get_model().indexable.base_queryset()


    def prepare_pVi(self, obj):
        if obj.vendor:
            return obj.vendor.image.url if obj.vendor.image else ''
        return ''
    
    def prepare_pStar(self, obj):
        return obj.get_ratings()
    
    def prepare_pDM(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'duration_months', 0)

    def prepare_pDD(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'duration_days', 0)

    def prepare_pRD(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'requires_delivery', False)

    def prepare_pCert(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'certification', False)

    def prepare_pEX(self, obj):
        if obj.is_service or obj.is_writing:
            return str(getattr(obj.attr, 'experience', None)) if getattr(obj.attr, 'experience', None) else None

    def prepare_pSM(self, obj):
        if obj.is_course:
            return str(getattr(obj.attr, 'study_mode', None)) if getattr(obj.attr, 'study_mode', None) else None

    def prepare_pCL(self, obj):
        if obj.is_course:
            return str(getattr(obj.attr, 'course_level', None)) if getattr(obj.attr, 'course_level', None) else None

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

    def prepare_pCts(self, obj):
        countries = obj.countries.all()
        if len(countries) > 0:
            return [con.code2 for con in countries]
    
    def prepare_pCtg(self, obj):
        categories = obj.categories.filter(
            productcategories__active=True,
            active=True)
        if len(categories) > 0:
            return [cat.name for cat in categories]

    def prepare_pFA(self, obj):
        categories = obj.categories.filter(
            productcategories__active=True,
            active=True)
        if len(categories) > 0:
            p_category = [pcat for cat in categories for pcat in cat.get_parent()]
            pp_category = [pcat for cat in p_category for pcat in cat.get_parent()]
            parents = [p_category, pp_category]
            return [item.name for sublist in parents for item in sublist if sublist]
