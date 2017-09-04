import json
from haystack import indexes
from .models import Product
from django.template.loader import render_to_string
from shop.choices import DURATION_DICT, convert_to_month
from shop.choices import (
    DURATION_DICT, convert_to_month)

def get_attributes(pv, currency='INR'):
    SM, CL, CERT, DM, PI = '', '', '', '', '' 
    if pv:
        SM = pv.get_studymode()
        CL = pv.get_courselevel()
        CERT = 'CERT1' if pv.get_cert() else 'CERT0'
        DM = pv.get_duration()
        if currency == 'INR':
            PI = pv.get_inr_price()
        elif currency == 'USD':
            PI = pv.get_usd_price()
        elif currency == 'AED':
            PI = pv.get_aed_price()
        elif currency == 'GBP':
            PI = pv.get_gbp_price()
        
    return 'SM'+ str(SM) + ' ' + 'CL' + str(CL) + ' '\
        + str(CERT)+ ' ' + 'DM' + str(DM)+ ' ' + 'P' + str(PI)


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
    pAR = indexes.FloatField(default=0, faceted=True)
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

    ##### Prices
    ### Flat normalised array for filter on variations
    pPinr = indexes.MultiValueField(faceted=True)
    pPusd = indexes.MultiValueField(faceted=True)
    pPaed = indexes.MultiValueField(faceted=True)
    pPgbp = indexes.MultiValueField(faceted=True)

    ### Calculated price of base + min var OR standalaone OR combos
    pPin = indexes.FloatField(indexed=False)
    pPfin = indexes.FloatField(indexed=False)
    pPus = indexes.FloatField(indexed=False)
    pPfus = indexes.FloatField(indexed=False)
    pPae = indexes.FloatField(indexed=False)
    pPfae = indexes.FloatField(indexed=False)
    pPgb = indexes.FloatField(indexed=False)
    pPfgb = indexes.FloatField(indexed=False)

    ### DB price of each object
    pPinb = indexes.FloatField(model_attr='inr_price', indexed=False)
    pPfinb = indexes.FloatField(model_attr='fake_inr_price', indexed=False)
    pPusb = indexes.FloatField(model_attr='usd_price', indexed=False)
    pPfusb = indexes.FloatField(model_attr='fake_usd_price', indexed=False)
    pPaeb = indexes.FloatField(model_attr='aed_price', indexed=False)
    pPfaeb = indexes.FloatField(model_attr='fake_aed_price', indexed=False)
    pPgbb = indexes.FloatField(model_attr='gbp_price', indexed=False)
    pPfgbb = indexes.FloatField(model_attr='fake_gbp_price', indexed=False)

    pAbx = indexes.CharField(model_attr='about', default='', indexed=False) 
    pARx = indexes.FloatField(model_attr='avg_rating', indexed=False)
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
            elif obj.type_product == 3:
                cmbs =list()
                cmbs = obj.get_combos()
                for cmb in cmbs:
                    DM.append(cmb.get_duration())
            else:
                DM.append(obj.get_duration())
            return list(set(DM))
        return []

    def prepare_pCert(self, obj):
        if obj.is_course:
            CERT = list()
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    CERT.append(pv.get_cert())
            elif obj.type_product == 3:
                cmbs =list()
                cmbs = obj.get_combos()
                for cmb in cmbs:
                    CERT.append(cmb.get_cert())
            else:
                CERT.append(obj.get_cert())
            return list(set(CERT))
        return []

    def prepare_pStM(self, obj):
        if obj.is_course:
            SM = list()
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    SM.append(pv.get_studymode())
            elif obj.type_product == 3:
                cmbs =list()
                cmbs = obj.get_combos()
                for cmb in cmbs:
                    SM.append(cmb.get_studymode())
            else:
                SM.append(obj.get_studymode())
            return list(set(SM))
        return []

    def prepare_pCL(self, obj):
        if obj.is_course:
            CL = []
            if obj.type_product == 1:
                var = obj.get_variations()
                for pv in var:
                    CL.append(pv.get_courselevel())
            elif obj.type_product == 3:
                cmbs =list()
                cmbs = obj.get_combos()
                for cmb in cmbs:
                    CL.append(cmb.get_courselevel())
            else:
                CL.append(obj.get_courselevel())
            return list(set(CL))
        return []

    def prepare_pPin(self, obj):
        Pinr = obj.inr_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.inr_price < var_price) or not var_price:
                    var_price = pv.inr_price
            if var_price:
                Pinr += var_price
        return Pinr

    def prepare_pPus(self, obj):
        Pusd = obj.usd_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.usd_price < var_price) or not var_price:
                    var_price = pv.usd_price
            if var_price:
                Pusd += var_price
        return Pusd

    def prepare_pPae(self, obj):
        Paed = obj.aed_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.aed_price < var_price) or not var_price:
                    var_price = pv.aed_price
            if var_price:
                Paed += var_price
        return Paed

    def prepare_pPfin(self, obj):
        Pinr = obj.fake_inr_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.fake_inr_price < var_price) or not var_price:
                    var_price = pv.fake_inr_price
            if var_price:
                Pinr += var_price
        return Pinr

    def prepare_pPfus(self, obj):
        Pusd = obj.fake_usd_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.fake_usd_price < var_price) or not var_price:
                    var_price = pv.fake_usd_price
            if var_price:
                Pusd += var_price
        return Pusd

    def prepare_pPfae(self, obj):
        Paed = obj.fake_aed_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.fake_aed_price < var_price) or not var_price:
                    var_price = pv.fake_aed_price
            if var_price:
                Paed += var_price
        return Paed

    def prepare_pPfgb(self, obj):
        Pgbp = obj.fake_gbp_price
        if obj.type_product == 1 and (obj.is_writing or obj.is_service):
            var = obj.get_variations()
            var_price = None
            for pv in var:
                if (var_price and pv.fake_gbp_price < var_price) or not var_price:
                    var_price = pv.fake_gbp_price
            if var_price:
                Pgbp += var_price
        return Pgbp

    def prepare_pPinr(self, obj):
        Pinr = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Pinr.append(pv.get_inr_price())
        else:
            Pinr.append(obj.get_inr_price())
        return list(set(Pinr))

    def prepare_pPusd(self, obj):
        Pusd = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Pusd.append(pv.get_usd_price())
        else:
            Pusd.append(obj.get_usd_price())
        return list(set(Pusd))

    def prepare_pPaed(self, obj):
        Paed = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Paed.append(pv.get_aed_price())
        else:
            Paed.append(obj.get_aed_price())
        return list(set(Paed))

    def prepare_pPgbp(self, obj):
        Pgbp = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                Pgbp.append(pv.get_gbp_price())
        else:
            Pgbp.append(obj.get_gbp_price())
        return list(set(Pgbp))

    def prepare_pAttrINR(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                ATTR.append(get_attributes(pv=pv,currency='INR'))
        elif obj.type_product == 3:
            cmbs =list()
            cmbs = obj.get_combos()
            for cmb in cmbs:
                ATTR.append(get_attributes(pv=cmb,currency='INR'))
        else:
            ATTR.append(get_attributes(pv=obj,currency='INR'))
        return list(set(ATTR))

    def prepare_pAttrUSD(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                ATTR.append(get_attributes(pv=pv,currency='USD'))
        elif obj.type_product == 3:
            cmbs =list()
            cmbs = obj.get_combos()
            for cmb in cmbs:
                ATTR.append(get_attributes(pv=cmb,currency='USD'))
        else:
            ATTR.append(get_attributes(pv=obj,currency='USD'))
        return list(set(ATTR))

    def prepare_pAttrAED(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                ATTR.append(get_attributes(pv=pv,currency='AED'))
        elif obj.type_product == 3:
            cmbs =list()
            cmbs = obj.get_combos()
            for cmb in cmbs:
                ATTR.append(get_attributes(pv=cmb,currency='AED'))
        else:
            ATTR.append(get_attributes(pv=obj,currency='AED'))
        return list(set(ATTR))

    def prepare_pAttrGBP(self, obj):
        ATTR = list()
        if obj.type_product == 1:
            var = obj.get_variations()
            for pv in var:
                ATTR.append(get_attributes(pv=pv,currency='GBP'))
        elif obj.type_product == 3:
            cmbs =list()
            cmbs = obj.get_combos()
            for cmb in cmbs:
                ATTR.append(get_attributes(pv=cmb,currency='GBP'))
        else:
            ATTR.append(get_attributes(pv=obj,currency='GBP'))
        return list(set(ATTR))

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
                        'level': pv.get_courselevel(),
                        'certify': pv.get_cert(),
                        'inrp': pv.get_inr_price(),
                        'aedp': pv.get_aed_price(),
                        'usdp': pv.get_usd_price(),
                        'gbpp': pv.get_gbp_price(),
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
                            'inrp': pv.get_inr_price(),
                            'aedp': pv.get_aed_price(),
                            'usdp': pv.get_usd_price(),
                            'gbpp': pv.get_gbp_price(),
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
    

