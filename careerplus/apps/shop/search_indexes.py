import json
from haystack import indexes
from .models import Product
from django.template.loader import render_to_string
from shop.choices import DURATION_DICT, convert_to_month
from shop.choices import (
    DURATION_DICT, convert_to_month,
    COURSE_ATTRIBUTE_DICT,
    RESUME_ATTRIBUTE_DICT,
    SERVICE_ATTRIBUTE_DICT)

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True, use_template=True,
        template_name='search/indexes/shop/product_text.txt')
    id = indexes.IntegerField(model_attr='id')
    
    # Search Fields #
    pHd = indexes.CharField(model_attr='heading', null=True)
    pFA = indexes.MultiValueField(null=True, faceted=True)
    pFAn = indexes.MultiValueField(null=True)
    pCtg = indexes.MultiValueField(null=True)
    pCtgn = indexes.MultiValueField(null=True)
    pCC = indexes.CharField(null=True)    
    pAb = indexes.CharField(default='') 
    
    # Meta and SEO #
    pURL = indexes.CharField(null=True, indexed=False)
    pTt = indexes.CharField(model_attr='title', null=True, indexed=False)
    pMtD = indexes.CharField(model_attr='meta_desc', null=True, indexed=False) 
    pMK = indexes.CharField(model_attr='meta_keywords', null=True, indexed=False) 
    
    # Control Field #
    pNm = indexes.CharField(model_attr='name', null=True)
    pSg = indexes.CharField(model_attr='slug', null=True)
    pTP = indexes.IntegerField(model_attr='type_product', default=0)
    pTF = indexes.IntegerField(model_attr='type_flow', default=0)
    pUPC = indexes.CharField(model_attr='upc', null=True, indexed=False)
    pPc = indexes.CharField(null=True)
    pPv = indexes.IntegerField(null=True)
    pPvn = indexes.CharField(null=True)
    pCts = indexes.MultiValueField(null=True)
    
    # Facets Fields #
    pAR = indexes.DecimalField(default=0, faceted=True)
    pStM = indexes.MultiValueField(null=True, faceted=True)
    pDM = indexes.MultiValueField(default=0, faceted=True)
    pCert = indexes.MultiValueField(default=False, faceted=True)
    pCL = indexes.MultiValueField(null=True, faceted=True)
    pAttrINR = indexes.MultiValueField(null=True)
    pAttrUSD = indexes.MultiValueField(null=True)
    pAttrAED = indexes.MultiValueField(null=True)
    pAttrGBP = indexes.MultiValueField(null=True)
    
    # Content Field #
    pIc = indexes.CharField(indexed=False)
    pIBg = indexes.IntegerField(default=0, indexed=False)
    pImg = indexes.CharField(indexed=False)
    pImA = indexes.CharField(model_attr='image_alt', null=True, indexed=False) 
    pvurl = indexes.CharField(indexed=False) # model_attr='video_url'
    pDsc = indexes.CharField(model_attr='description', indexed=False) 
    pBS = indexes.CharField(model_attr='buy_shine', indexed=False) 
    pStar = indexes.MultiValueField(null=True, indexed=False)
    pRC = indexes.IntegerField(model_attr='no_review', default=0, indexed=False) 
    pBC = indexes.IntegerField(model_attr='buy_count', default=0, indexed=False) 
    pNJ = indexes.IntegerField(model_attr='num_jobs', default=0, indexed=False) 

    pVi = indexes.CharField(null=True, indexed=False)
    pCT = indexes.CharField(null=True, indexed=False)
    pDD = indexes.IntegerField(default=0, indexed=False)
    pRD = indexes.BooleanField(default=True, indexed=False)
    pEX = indexes.CharField(null=True, indexed=False)

    # Prices
    pPinr = indexes.MultiValueField(faceted=True)
    pPusd = indexes.MultiValueField(faceted=True)
    pPaed = indexes.MultiValueField(faceted=True)
    pPgbp = indexes.MultiValueField(faceted=True)


    pAbx = indexes.CharField(model_attr='about', default='', indexed=False) 
    pARx = indexes.DecimalField(model_attr='avg_rating', indexed=False) 
    pFAQs = indexes.CharField(indexed=False)
    pPChs = indexes.CharField(indexed=False)
    pCmbs = indexes.CharField(indexed=False)
    pVrs = indexes.CharField(indexed=False)
    pFBT = indexes.CharField(indexed=False)
    pPOP = indexes.CharField(indexed=False)
    pCD = indexes.DateTimeField(model_attr='created', indexed=True)
    pMD = indexes.DateTimeField(model_attr='modified', indexed=False)
    
    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().indexable.all()

    def read_queryset(self, using=None):
        return self.get_model().indexable.base_queryset()

    def prepare_pCtg(self, obj):
        categories = obj.categories.filter(
            productcategories__active=True,
            active=True)
        if len(categories) > 0:
            return [cat.pk for cat in categories]
        
    def prepare_pCtgn(self, obj):
        categories = obj.categories.filter(
            productcategories__active=True,
            active=True)
        if len(categories) > 0:
            return [cat.name for cat in categories]
        
    def prepare_pFA(self, obj):
        if obj.is_course:    
            categories = obj.categories.filter(
                productcategories__active=True,
                active=True)
            if len(categories) > 0:
                p_category = [pcat for cat in categories for pcat in cat.get_parent()]
                # pp_category = [pcat for cat in p_category for pcat in cat.get_parent()]
                parents = [p_category,]
                return [item.pk for sublist in parents for item in sublist if sublist]
        return []

    def prepare_pFAn(self, obj):
        if obj.is_course:    
            categories = obj.categories.filter(
                productcategories__active=True,
                active=True)
            if len(categories) > 0:
                p_category = [pcat for cat in categories for pcat in cat.get_parent()]
                # pp_category = [pcat for cat in p_category for pcat in cat.get_parent()]
                parents = [p_category,]
                return [item.name for sublist in parents for item in sublist if sublist]
        return []

    def prepare_pCC(self, obj):
        content = ''
        chapters = obj.chapter_product.filter(status=True)\
                .order_by('ordering')
        chapter_list = []
        if chapters:
            for pch in chapters:
                chapter_list.append({
                    'heading': pch.heading,
                    'content': pch.answer,
                })
            content = render_to_string(
                'search/indexes/shop/course_content.html',
                {"chap_list": chapter_list})
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                strpcontent = soup.get_text()
            except:
                strpcontent = content
            return strpcontent
        return ''

    def prepare_pAb(self, obj):
        if obj.about:    
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(obj.about, 'html.parser')
                strpcontent = soup.get_text()
            except:
                strpcontent = obj.about
            return strpcontent
        return ''

    def prepare_pAR(self, obj):
        return obj.get_avg_ratings()

    def prepare_pDM(self, obj):
        if obj.is_course:
            DM = []
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    DM.append(pv.get_duration())
                DM = list(set(DM))
            else:
                DM.append(obj.get_duration())
            return DM
        return []

    def prepare_pCert(self, obj):
        if obj.is_course:
            CERT = list()
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    CERT.append(pv.get_cert())
                CERT = list(set(CERT))
            else:
                CERT.append(obj.get_cert())
            return CERT
        return []

    def prepare_pStM(self, obj):
        if obj.is_course:
            SM = list()
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    SM.append(pv.get_studymode())
                SM = list(set(SM))
            else:
                SM.append(obj.get_studymode())
            return SM
        return []

    def prepare_pCL(self, obj):
        if obj.is_course:
            CL = []
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    CL.append(pv.get_courselevel())
                CL = list(set(CL))
            else:
                CL.append(obj.get_courselevel())
            return CL
        return []

    def prepare_pPinr(self, obj):
        Pinr = list()
        Pinr.append(obj.get_inr_price())
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Pinr.append(pv.get_inr_price())
            Pinr = list(set(Pinr))
        return Pinr

    def prepare_pPusd(self, obj):
        Pusd = list()
        Pusd.append(obj.get_usd_price())
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Pusd.append(pv.get_usd_price())
            Pusd = list(set(Pusd))
        return Pusd

    def prepare_pPaed(self, obj):
        Paed = list()
        Paed.append(obj.get_aed_price())
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Paed.append(pv.get_aed_price())
            Paed = list(set(Paed))
        return Paed

    def prepare_pPgbp(self, obj):
        Pgbp = list()
        Pgbp.append(obj.get_gbp_price())
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Pgbp.append(pv.get_gbp_price())
            Pgbp = list(set(Pgbp))
        return Pgbp

    def prepare_pAttrINR(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                SM = pv.get_studymode()
                CL = pv.get_courselevel()
                CERT = 'CERT1' if pv.get_cert() else 'CERT0'
                DM = pv.get_duration()
                PI = pv.get_inr_price()
                ATTR.append(
                    'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                    + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PI))
        else:
            SM = obj.get_studymode()
            CL = obj.get_courselevel()
            CERT = 'CERT1' if obj.get_cert() else 'CERT0'
            DM = obj.get_duration()
            PI = obj.get_inr_price()
            ATTR.append(
                'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PI))
        return ATTR

    def prepare_pAttrUSD(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                SM = pv.get_studymode()
                CL = pv.get_courselevel()
                CERT = 'CERT1' if pv.get_cert() else 'CERT0'
                DM = pv.get_duration()
                PU = pv.get_usd_price()
                ATTR.append(
                    'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                    + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PU))
        else:
            SM = obj.get_studymode()
            CL = obj.get_courselevel()
            CERT = 'CERT1' if obj.get_cert() else 'CERT0'
            DM = obj.get_duration()
            PU = obj.get_usd_price()
            ATTR.append(
                'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PU))
        return ATTR

    def prepare_pAttrAED(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                SM = pv.get_studymode()
                CL = pv.get_courselevel()
                CERT = 'CERT1' if pv.get_cert() else 'CERT0'
                DM = pv.get_duration()
                PA = pv.get_aed_price()
                ATTR.append(
                    'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                    + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PA))
        else:
            SM = obj.get_studymode()
            CL = obj.get_courselevel()
            CERT = 'CERT1' if obj.get_cert() else 'CERT0'
            DM = obj.get_duration()
            PA = obj.get_aed_price()
            ATTR.append(
                'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PA))
        return ATTR

    def prepare_pAttrGBP(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                SM = pv.get_studymode()
                CL = pv.get_courselevel()
                CERT = 'CERT1' if pv.get_cert() else 'CERT0'
                DM = pv.get_duration()
                PG = pv.get_gbp_price()
                ATTR.append(
                    'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                    + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PG))
        else:
            SM = obj.get_studymode()
            CL = obj.get_courselevel()
            CERT = 'CERT1' if obj.get_cert() else 'CERT0'
            DM = obj.get_duration()
            PG = obj.get_gbp_price()
            ATTR.append(
                'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
                + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PG))
        return ATTR

    def prepare_pCT(self, obj):
        return obj.get_coursetype()

    def prepare_pURL(self, obj):
        return obj.get_url(relative=True) if obj.get_url(relative=True) else ''

    def prepare_pPc(self, obj):
        return obj.product_class.slug if obj.product_class else ''

    def prepare_pPv(self, obj):
        return obj.vendor.pk if obj.vendor else None

    def prepare_pPvn(self, obj):
        return obj.vendor.name if obj.vendor else ''

    def prepare_pCts(self, obj):
        countries = obj.countries.all()
        if len(countries) > 0:
            return [con.code2 for con in countries]
    
        
    def prepare_pIc(self, obj):
        return obj.get_icon_url(relative=True)
        
    def prepare_pImg(self, obj):
        return obj.get_image_url(relative=True)

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
    
    def prepare_pRD(self, obj):
        if obj.is_course:
            return getattr(obj.attr, 'requires_delivery', False)
    
    def prepare_pEX(self, obj):
        return obj.get_exp()
    
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
                    'url': cmb.get_url(relative=True)
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
                        'mode': pv.get_studymode(),
                        'duration': pv.get_duration(),
                        'type': pv.get_coursetype(),
                        'certify': pv.get_cert(),
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
                            'country': pv.get_profile_country(),
                            'experience': pv.get_exp(),
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
                fbt_dict.update({
                    'fbt': True
                })
                
            for pv in fbt:
                if pv.is_course:    
                    fbt_list.append({
                        'id': pv.id,
                        'label': pv.name,
                        'mode': pv.get_studymode(),
                        'duration': pv.get_duration(),
                        'type': pv.get_coursetype(),
                        'certify': pv.get_cert(),
                        'inr_price': float(pv.inr_price),
                        'fake_inr_price': float(pv.fake_inr_price),
                        'usd_price': float(pv.usd_price),
                        'fake_usd_price': float(pv.fake_usd_price),
                        'aed_price': float(pv.aed_price),
                        'fake_aed_price': float(pv.fake_aed_price),
                        'gbp_price': float(pv.gbp_price),
                        'fake_gbp_price': float(pv.fake_gbp_price)})
                elif pv.is_writing or pv.is_service:
                    fbt_list.append({
                        'id': pv.id,
                        'label': pv.name,
                        'country': pv.get_profile_country(),
                        'experience': pv.get_exp(),
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
                        'url': pv.get_url(relative=True),
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
                            'experience': pv.get_exp(),
                            'url': pv.get_url(relative=True),
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
    

