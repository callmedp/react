import json
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
    pHd = indexes.EdgeNgramField(model_attr='heading', null=True,)
    pHdx = indexes.CharField(model_attr='heading', null=True, indexed=False) 
    
    # Control Field #
    pNm = indexes.CharField(model_attr='name', null=True)
    pSg = indexes.CharField(model_attr='slug', null=True)
    pTP = indexes.IntegerField(model_attr='type_product', default=0)
    pTF = indexes.IntegerField(model_attr='type_flow', default=0)
    pUPC = indexes.CharField(model_attr='upc', null=True, indexed=False)
    
    # Content Field#
    pIc = indexes.CharField(indexed=False)
    pIBg = indexes.IntegerField(default=0, indexed=False)
    pImg = indexes.CharField(indexed=False)
    pImA = indexes.CharField(model_attr='image_alt', null=True, indexed=False) 
    pvurl = indexes.CharField(indexed=False) # model_attr='video_url'
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
    pCL = indexes.CharField(null=True, faceted=True)
    
    pStar = indexes.CharField(null=True, indexed=False)
    pRC = indexes.IntegerField(model_attr='no_review', default=0, indexed=False) 
    pBC = indexes.IntegerField(model_attr='buy_count', default=0, indexed=False) 
    pNJ = indexes.IntegerField(model_attr='num_jobs', default=0, indexed=False) 
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
    
    pFAQs = indexes.CharField(indexed=False)
    pPChs = indexes.CharField(indexed=False)
    
    pCmbs = indexes.CharField(indexed=False)
    pVrs = indexes.CharField(indexed=False)
    pFBT = indexes.CharField(indexed=False)
    pPOP = indexes.CharField(indexed=False)
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

    def prepare_pURL(self, obj):
        return obj.get_url() if obj.get_url() else ''
        
    def prepare_pIc(self, obj):
        return obj.get_icon_url()
        
    def prepare_pImg(self, obj):
        return obj.get_image_url()

    def prepare_pIBg(self, obj):
        return obj.image_bg
    
    def prepare_pImA(self, obj):
        return obj.image_alt
        
    def prepare_pvurl(self, obj):
        return obj.video_url
    
    def prepare_pStar(self, obj):
        return obj.get_ratings()
    
    def prepare_pVi(self, obj):
        if obj.vendor:
            return obj.vendor.image.url if obj.vendor.image else ''
        return ''
    
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
            return getattr(obj.attr, 'experience', None) if getattr(obj.attr, 'experience', None) else None

    def prepare_pSM(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'study_mode', None) if getattr(obj.attr, 'study_mode', None) else None

    def prepare_pCL(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'course_level', None) if getattr(obj.attr, 'course_level', None) else None

    def prepare_pCT(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'course_type', None) if getattr(obj.attr, 'course_type', None) else None

    def prepare_pPc(self, obj):
        return obj.product_class.slug if obj.product_class else ''

    def prepare_pPv(self, obj):
        return obj.vendor.name if obj.vendor else ''

    def prepare_pCts(self, obj):
        countries = obj.countries.all()
        if len(countries) > 0:
            return [con.code2 for con in countries]
    
    def prepare_pCtg(self, obj):
        if obj.is_course:
            categories = obj.categories.filter(
                productcategories__active=True,
                active=True)
            if len(categories) > 0:
                return [cat.name for cat in categories]
        return []
    def prepare_pFA(self, obj):
        if obj.is_course:    
            categories = obj.categories.filter(
                productcategories__active=True,
                active=True)
            if len(categories) > 0:
                p_category = [pcat for cat in categories for pcat in cat.get_parent()]
                pp_category = [pcat for cat in p_category for pcat in cat.get_parent()]
                parents = [p_category, pp_category]
                return [item.name for sublist in parents for item in sublist if sublist]
        return []
    
    def prepare_pFAQs(self, obj):
        structure = {
            'faq': False
        }
        faqs = obj.faqs.filter(
            productfaqs__active=True, status=2)\
                .order_by('productfaqs__question_order') 
        faq_list = []
        if faqs:
            structure.update({
                'faq': True
            })
            for pfq in faqs:
                faq_list.append({
                    'question': pfq.text,
                    'answer': pfq.answer
                })
            structure.update({
                'faq_list': faq_list
            })
        return json.dumps(structure)

    def prepare_pCmbs(self, obj):
        combo_dict = {
            'combo': False,
            'combo_list': []
        }
        combo_list = []
        if obj.type_product == 3:    
            combos = obj.get_combos()
        else:
            return json.dumps(combo_dict) 
        if combos:
            combo_dict.update({
                'combo': True
            })
            for cmb in combos:
                combo_list.append({
                    'pk': cmb.pk,
                    'name': cmb.heading,
                    'url': cmb.get_url()
                })
            combo_dict.update({
                'combo_list': combo_list
            })
        return json.dumps(combo_dict)

    def prepare_pVrs(self, obj):
        var_dict = {
            'variation': False,
            'var_list': []
        }
        var_list = []
        if obj.type_product == 1:
            var = obj.get_variations()
        else:
            return json.dumps(var_dict) 
        if var:
            if obj.is_course:
                var_dict.update({
                    'variation': True
                })
                for pv in var:
                    var_list.append({
                        'id': pv.id,
                        'label': pv.name,
                        'mode': str(getattr(pv.attr, 'study_mode', '')),
                        'duration': str(getattr(pv.attr, 'duration_months', '')),
                        'type': str(getattr(pv.attr, 'course_type', '')),
                        'certify': str(getattr(pv.attr, 'certification', '')),
                        'inr_price': float(pv.inr_price),
                        'fake_inr_price': float(pv.fake_inr_price),
                        'usd_price': float(pv.usd_price),
                        'fake_usd_price': float(pv.fake_usd_price),
                        'aed_price': float(pv.aed_price),
                        'fake_aed_price': float(pv.fake_aed_price),
                        'gbp_price': float(pv.gbp_price),
                        'fake_gbp_price': float(pv.fake_gbp_price)})
                var_dict.update({
                    'var_list': var_list
                })
            elif obj.is_writing or obj.is_service:
                var_dict.update({
                    'variation': True
                })
                for pv in var:
                    for pv in var:
                        var_list.append({
                            'id': pv.id,
                            'label': pv.name,
                            'country': str(getattr(pv.attr, 'profile_country', '')),
                            'experience': str(getattr(pv.attr, 'experience', None)),
                            'inr_price': float(pv.inr_price),
                            'fake_inr_price': float(pv.fake_inr_price),
                            'usd_price': float(pv.usd_price),
                            'fake_usd_price': float(pv.fake_usd_price),
                            'aed_price': float(pv.aed_price),
                            'fake_aed_price': float(pv.fake_aed_price),
                            'gbp_price': float(pv.gbp_price),
                            'fake_gbp_price': float(pv.fake_gbp_price)})
                var_dict.update({
                    'var_list': var_list
                })
        return json.dumps(var_dict)

    def prepare_pPChs(self, obj):
        structure = {
            'chapter': False
        }
        chapters = obj.chapter_product.filter(status=True)\
                .order_by('ordering')
        chapter_list = []
        if chapters:
            structure.update({
                'chapter': True
            })
            for pch in chapters:
                chapter_list.append({
                    'heading': pch.heading,
                    'content': pch.answer,
                    'ordering': pch.ordering
                })
            structure.update({
                'chapter_list': chapter_list
            })
        return json.dumps(structure)

    def prepare_pFBT(self, obj):
        fbt_dict = {
            'fbt': False,
            'fbt_list': []
        }
        fbt_list = []
        fbt = obj.get_fbts() 
        if fbt:
            if obj.is_course:
                fbt_dict.update({
                    'fbt': True
                })
                for pv in fbt:
                    fbt_list.append({
                        'id': pv.id,
                        'label': pv.name,
                        'mode': str(getattr(pv.attr, 'study_mode', '')),
                        'duration': str(getattr(pv.attr, 'duration_months', '')),
                        'type': str(getattr(pv.attr, 'course_type', '')),
                        'certify': str(getattr(pv.attr, 'certification', '')),
                        'inr_price': float(pv.inr_price),
                        'fake_inr_price': float(pv.fake_inr_price),
                        'usd_price': float(pv.usd_price),
                        'fake_usd_price': float(pv.fake_usd_price),
                        'aed_price': float(pv.aed_price),
                        'fake_aed_price': float(pv.fake_aed_price),
                        'gbp_price': float(pv.gbp_price),
                        'fake_gbp_price': float(pv.fake_gbp_price)})
                fbt_dict.update({
                    'fbt_list': fbt_list
                })
            elif obj.is_writing or obj.is_service:
                fbt_dict.update({
                    'fbt': True
                })
                for pv in fbt:
                    for pv in fbt:
                        fbt_list.append({
                            'id': pv.id,
                            'label': pv.name,
                            'country': str(getattr(pv.attr, 'profile_country', '')),
                            'experience': str(getattr(pv.attr, 'experience', None)),
                            'inr_price': float(pv.inr_price),
                            'fake_inr_price': float(pv.fake_inr_price),
                            'usd_price': float(pv.usd_price),
                            'fake_usd_price': float(pv.fake_usd_price),
                            'aed_price': float(pv.aed_price),
                            'fake_aed_price': float(pv.fake_aed_price),
                            'gbp_price': float(pv.gbp_price),
                            'fake_gbp_price': float(pv.fake_gbp_price)})
                fbt_dict.update({
                    'fbt_list': fbt_list
                })
        return json.dumps(fbt_dict)

    def prepare_pPOP(self, obj):
        pop_dict = {
            'pop': False,
            'pop_list': []
        }
        pop_list = []
        pop = obj.get_pops() 
        if pop:
            if obj.is_course:
                pop_dict.update({
                    'pop': True
                })
                for pv in pop:
                    pop_list.append({
                        'id': pv.id,
                        'label': pv.name,
                        'vendor': pv.vendor.name,
                        'url': pv.get_url(),
                        'inr_price': float(pv.inr_price),
                        'fake_inr_price': float(pv.fake_inr_price),
                        'usd_price': float(pv.usd_price),
                        'fake_usd_price': float(pv.fake_usd_price),
                        'aed_price': float(pv.aed_price),
                        'fake_aed_price': float(pv.fake_aed_price),
                        'gbp_price': float(pv.gbp_price),
                        'fake_gbp_price': float(pv.fake_gbp_price)})
                pop_dict.update({
                    'pop_list': pop_list
                })
            elif obj.is_writing or obj.is_service:
                pop_dict.update({
                    'pop': True
                })
                for pv in pop:
                    for pv in pop:
                        pop_list.append({
                            'id': pv.id,
                            'label': pv.name,
                            'experience': str(getattr(pv.attr, 'experience', None)),
                            'url': pv.get_url(),
                            'inr_price': float(pv.inr_price),
                            'fake_inr_price': float(pv.fake_inr_price),
                            'usd_price': float(pv.usd_price),
                            'fake_usd_price': float(pv.fake_usd_price),
                            'aed_price': float(pv.aed_price),
                            'fake_aed_price': float(pv.fake_aed_price),
                            'gbp_price': float(pv.gbp_price),
                            'fake_gbp_price': float(pv.fake_gbp_price)})
                pop_dict.update({
                    'pop_list': pop_list
                })
        return json.dumps(pop_dict)
        