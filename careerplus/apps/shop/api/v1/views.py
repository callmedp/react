# python imports
import logging

# django imports
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.text import slugify  
from django.conf import settings



# local imports
from .serializers import (
    ProductListSerializerForAuditHistory,
    ProductDetailSerializer,
    PracticeTestInfoCreateSerializer,
    UpdateProductScreenSkillSerializer,
    UpdateProductSkillSerializer)
from django.contrib.contenttypes.models import ContentType

from .tasks import delete_from_solr, update_practice_test_info

# interapp imports
from shop.models import (Product, ProductScreen, PracticeTestInfo, Skill, FunctionalArea,ProductSkill)
from shared.permissions import HasGroupOrHasPermissions
from shop.api.core.permissions import IsVendorAssociated
from shared.rest_addons.mixins import FieldFilterMixin
from shop.helpers import get_inferred_skills
from shared.rest_addons.authentication import ShineUserAuthentication
from core.api_mixin import ShineCandidateDetail
from search.helpers import get_recommended_products
from skillpage.api.v1.serializers import LoadMoreSerializerSolr
from shared.rest_addons.pagination import LearningCustomPagination
from shared.rest_addons.mixins import FieldFilterMixin
from review.models import Review
from partner.models import Certificate,ProductSkill


# 3rd party imports
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from shop.mixins import SkillProducts

class ProductListView(FieldFilterMixin, ListAPIView):
    serializer_class = ProductListSerializerForAuditHistory
    authentication_classes = (SessionAuthentication,)
    # filter_backends = (DjangoFilterBackend,)
    permission_classes = (HasGroupOrHasPermissions, IsVendorAssociated,)
    permission_groups = []
    permission_code_name = []

    def get_queryset(self):
        """
        Return product List only if any of filter fields is present in
        query params.

        category_id = Category id to be added
        vendor_id = Multiple vendor to be added with ',' separated
        type_flow = enter the product type flow

        """
        filter_dict = {}
        category_id = self.request.GET.get('category')
        vendor_id = self.request.GET.get('vendor')
        type_flow = self.request.GET.get('type_flow')
        type_query = self.request.GET.get('type')
        user = self.request.user
        vendor_id = vendor_id if vendor_id else user.vendor_set.values_list('id', flat=True)
        if category_id:
            filter_dict.update({'categories__id': category_id})
        if vendor_id and not user.is_superuser:
            vendor_id = vendor_id.split(',') if isinstance(vendor_id, str) else vendor_id
            filter_dict.update({'vendor__id__in': vendor_id})
        # else:
        #     return Product.objects.none()
        if type_flow:
            filter_dict.update({'type_flow': type_flow})

        if type_query and self.request.GET.get(type_query):
            if type_query == 'name':
                filter_dict.update({type_query + '__icontains': self.request.GET.get(type_query)})
            else:
                filter_dict.update({type_query: self.request.GET.get(type_query)})

        return Product.objects.filter(**filter_dict).exclude(type_flow=14)


class ProductDeleteView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        id_list = request.data.get('data', '')
        products = Product.objects.filter(slug__in=id_list)
        product_screens = ProductScreen.objects.filter(slug__in=id_list)
        product_count = 0
        product_screen_count = 0

        if products.exists() or product_screens.exists():
            # get product count
            product_count = len(products)

            # get product screen count
            product_screen_count = len(product_screens)

            # bulk deletion of the products

            if product_screen_count > 0:
                product_screens.delete()

            if product_count > 0:
                products.delete()

            delete_from_solr.delay()

        return Response({
            'message': '{} products deleted and {} product screens deleted'
            .format(product_count, product_screen_count)
            }, status=200)


class ProductDetailView(FieldFilterMixin, ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        filter_dict = {}
        category_id = self.request.GET.get('category')
        vendor_id = self.request.GET.get('vendor')
        type_flow = self.request.GET.get('type_flow')
        type_query = self.request.GET.get('type')

        if category_id:
            filter_dict.update({'categories__id': category_id})
        if vendor_id:
            vendor_id = vendor_id.split(',')
            filter_dict.update({'vendor__id__in': vendor_id})
        if type_flow:
            filter_dict.update({'type_flow': type_flow})

        if type_query and self.request.GET.get(type_query):
            if type_query == 'name':
                filter_dict.update({type_query + '__icontains': self.request.GET.get(type_query)})
            else:
                filter_dict.update({type_query: self.request.GET.get(type_query)})

        return Product.objects.filter(**filter_dict)


class CreatePracticeTestInfoAPIView(CreateAPIView):
    serializer_class = PracticeTestInfoCreateSerializer
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePracticeTestInfoAPIView, self).dispatch(request, *args, **kwargs)


class UpdatePracticeInfoApiView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdatePracticeInfoApiView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        if email:
            self.kwargs['email'] = email
        else:
            return Response({'email: Provide this field'}, status=status.HTTP_400_BAD_REQUEST)
        data = update_practice_test_info(email)
        if data:
            if data.get('status', None) != 400:
                if data['status'] == 'done':
                    session_id = request.session.session_key
                    cache.set('{}_neo_email_done'.format(session_id), email, 3600 * 24 * 30)
                    from .tasks import create_neo_lead
                    create_neo_lead.delay(email)
                return Response(data)
            else:
                return Response({
                    'message': 'Already Registered'.format(email)
                    }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'message': 'Invalid Email'.format(email)
            }, status=status.HTTP_400_BAD_REQUEST)


class BoardNeoProductApiView(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        from order.models import OrderItem
        from order.tasks import board_user_on_neo
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.data.get('oi_pk')
        if self.oi_pk and self.candidate_id:
            self.oi = OrderItem.objects.select_related("order").filter(pk=self.oi_pk).first()
            if (
                self.oi and self.oi.product.vendor.slug == 'neo'
                and self.oi.order.candidate_id == self.candidate_id
                and self.oi.order.status in [1, 3]
            ):
                if not self.oi.neo_mail_sent:
                    boarding_type = board_user_on_neo([self.oi.id])
                    msg = 'Please check you mail to confirm boarding on Neo'
                    if boarding_type == 'already_trial':
                        msg = 'You Account has been Updated from Trial To Regular'
                    return Response({'msg': msg})

        raise PermissionDenied


class ParseSkillFromTextApiView(APIView):
    """
    This APIView takes text as input and return
    parsed skills from text.
    """

    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        k = get_inferred_skills(text)
        return Response(data=k, status=status.HTTP_200_OK)


class UpdateScreenProductSkillView(CreateAPIView):
    """
    This API endpoint takes data in the format of
    {
        "user_type": [<skill_name1>,<skill_name2>],
        "product_type": [<skill_name3>,<skill_name4>],
        "product_id": <product_id>
    }
    and update skill for productscreen
    """
    serializer_class = UpdateProductScreenSkillSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )


class UpdateProductSkillView(CreateAPIView):
    """
    This API endpoint takes data in the format of
    {
        "user_type": [<skill_name1>,<skill_name2>],
        "product_type": [<skill_name3>,<skill_name4>],
        "product_id": <product_id>
    }
    and update skill for product
    """
    serializer_class = UpdateProductSkillSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )


class RecommendedProductsAPIView(FieldFilterMixin, ListAPIView):
    """
    This API  gives recommended products.
    Data required: {
        email: Email of candidate,
        fl: All the fileds required from solr
        }
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoadMoreSerializerSolr
    pagination_class = LearningCustomPagination

    def get_queryset(self, *args, **kwargs):
        email = self.request.GET.get('email', '')
        skills_ids = None
        func_area = None
        job_title = None

        candidate_detail = ShineCandidateDetail().get_candidate_public_detail(email=email)
        if candidate_detail:
            skills = [skill['value'] for skill in candidate_detail['skills']]
            skills_in_ascii = []
            for skill in skills:
                try:
                    skills_in_ascii.append(
                        skill.encode('ascii', 'replace').decode('ascii', 'replace')
                        )
                except Exception as e:
                    logging.getLogger('error_log').error(
                        'error in decrypting skills into ascii {}'.format(str(e))
                        )
                    skills_in_ascii.append("")
            # Settings all skill in sessions
            skills_obj = Skill.objects.filter(name__in=skills_in_ascii)
            skills_ids = [str(skill.id) for skill in skills_obj]

            candid_job_detail = candidate_detail.get('jobs')[0] if candidate_detail.get('jobs') \
                and isinstance(candidate_detail.get('jobs'), list) else None
            if candid_job_detail:
                func_area_detail = candid_job_detail.get("parent_sub_field", "")
                func_area_obj = FunctionalArea.objects.filter(
                    name__iexact=func_area_detail).first()
            if func_area_obj:
                func_area = func_area_obj.id
            if candid_job_detail and candid_job_detail.get('job_title'):
                job_title = str.title(candid_job_detail.get('job_title'))

        products = get_recommended_products(
            job_title=job_title, skills=skills_ids, func_area=func_area
            )

        return products


class ProductReview(APIView):
    authentication_classes = ()
    permission_classes = ()


    def post(self, request, *args, **kwargs) :
        """
        This method create reviews for individual product.
        """
        candidate_id = request.data.get('candidate_id', None)
        product_pk = request.data.get('product_id')
        review_id = request.data.get('review_id')
        email = request.data.get('email')
        name_full = request.data.get('full_name','')
        update_dict = {'status':0}

        if not candidate_id:
            return Response({'error':'unable to ppost review'},status=status.HTTP_400_BAD_REQUEST)

        data = {
            "display_message" : 'Thank you for posting a review. It will be displayed on the site after moderation',
            "success" : False
        }
        try:
            product = Product.objects.get(pk=product_pk)
            contenttype_obj = ContentType.objects.get_for_model(product)
            if review_id:
                review_obj = Review.objects.get(id=review_id)
            else:
                review_obj,created = Review.objects.get_or_create(
                    object_id=product.id,
                    content_type=contenttype_obj,
                    user_id=candidate_id
                )
            review = request.data.get('review', '').strip()
            rating = int(request.data.get('rating', 1))
            title = request.data.get('title', '')

            if rating and review_obj and product:

                if not review_obj.user_name:
                    update_dict.update({'user_name':name_full})
                if not review_obj.user_email:
                    if not email:
                        return Response({'error':'unable to review'},status=status.HTTP_400_BAD_REQUEST)
                    update_dict.update({'user_email':email})


                update_dict.update({'title':title,'average_rating':rating,'content':review,
                                    'extra_content_obj':contenttype_obj,'extra_object_id':product.id})

                for attr,value in update_dict.items():
                    setattr(review_obj,attr,value)
                review_obj.save()
                if settings.DEBUG:
                    product.save()

                return Response(data,status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'Something went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response({'error' : 'Something went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SkillProductView(SkillProducts,APIView):

    """
     Params  to be added 
     
     1) cert=1,2,3    [ comma separated certificate id to get the product according to certificate skill]
     
     2) skills = [ comma separated skills name or slug to get the product according to skills ]
     
     3) assessment = [Add this params as true or 1 to get the assessment type products]
    
     EX:= /api/v1/skill-product/?skills=java,javascript or
     /api/v1/skill-product/?cert=221,220&assessment=true


    """

    authentication_classes = ()
    permission_classes = ()

    # def get_product_from_skill(self,skill=[]):
    #     if not skill:
    #         return []
    #     filter_dict = {'active':True,'is_indexed':True,'is_indexable':True}
    #     product_id = None
    #     assessment = self.request.GET.get('assessment')
    #     if assessment:
    #         filter_dict.update({'type_flow':16})
    #     WhatYouGet = {
    #         'testpreptraining':[
    #         "Receive valuable feedback, from reliable exam reports, on your strong and weak areas",
    #         "Get real exam and practice environment",
    #         "In depth and exhaustive explanation to every question to enhance your learning",
    #             "Unlimited access to the assessment platform",
    #             "500+ questions to test your learning on variety of topics",
    #             "Gets Tips & Tricks to crack the test",
    #         ],
    #     }
    #
    #     if isinstance(skill,list):
    #         product_id = ProductSkill.objects.filter(skill__slug__in=skill).values_list('product_id',flat=True)
    #
    #     else:
    #         product_id = ProductSkill.objects.filter(skill__slug=skill).values_list('product_id',flat=True)
    #
    #     products = Product.objects.filter(id__in=product_id, **filter_dict)
    #
    #     data = []
    #
    #     for prod in products:
    #         data_dict = {}
    #         data_dict.update ({'id' : prod.id , 'heading' : prod.get_heading () , 'title' : prod.get_title () ,
    #                            'url' : prod.get_url () ,
    #                            'icon' : prod.get_icon_url () , 'about' : prod.get_about () ,
    #                            'img_url':prod.image.url if prod.image else '',
    #                            'inr_price' : prod.get_price () ,
    #                            'fake_inr_price' : prod.fake_inr_price , 'attribute' : prod.get_assessment_attribute () ,
    #                            'vendor' : prod.vendor_id})
    #         if prod.type_flow == 16 :
    #             if not prod.vendor :
    #                 data_dict.update ({
    #                     'what_you_get' : [
    #                         "Industry recognized certification after clearing the test" ,
    #                         "Get badge on shine.com and showcase your knowledge to the recruiters" ,
    #                         "Shine shows your skills as validated and certification as verified which build high trust "
    #                         "among recruiters" ,
    #                         "Receive valuable feedback on your strong and weak areas to improve yourself" ,
    #                         "Certified candidates gets higher salary as compared to non certified candidate"
    #                     ]
    #                 })
    #             else :
    #
    #                 data_dict.update ({
    #                     'what_you_get' : WhatYouGet.get (prod.vendor.slug , [
    #                         "Industry recognized certification after clearing the test" ,
    #                         "Get badge on shine.com and showcase your knowledge to the recruiters" ,
    #                         "Shine shows your skills as validated and certification as verified which build high trust "
    #                         "among recruiters" ,
    #                         "Receive valuable feedback on your strong and weak areas to improve yourself" ,
    #                         "Certified candidates gets higher salary as compared to non certified candidate"
    #                     ])
    #                 })
    #
    #         data.append (data_dict)
    #     return data

    def get(self,request,*args,**kwargs):
        certificate_id = self.request.GET.get('cert')
        skills = self.request.GET.get('skills',[])
        assessment = self.request.GET.get('assessment')
        vendors_list = self.request.GET.get('vendor')

        if vendors_list:
            vendors_list = vendors_list.split(',')
        else:
            vendors_list = []
        skill_list = []
        fl = self.request.GET.get('fl',[])
        if not fl:
            fl = []
        else:
            fl = fl.split(',')


        if certificate_id:
            certificate_products =[]
            certificate_id = certificate_id.split(',')
            certificate = Certificate.objects.only('id','skill').filter(id__in=certificate_id)
            if not certificate.exists():
                return Response({'data': []},status=status.HTTP_200_OK)
            for cert in certificate:
                if not cert.skill:
                    continue
                skills = list(map(slugify,cert.skill.split(',')))
                certificate_products.append({cert.id:self.get_product_from_skill(skills,fl)})

            return Response({'data':certificate_products},status=status.HTTP_200_OK)


        if skills and skills != 'all':
            skills = list(map(slugify,skills.split(',')))
            for skill in skills:
                skill_list.append({skill:self.get_product_from_skill(skill,fl)})
            return Response ({'data': skill_list}, status=status.HTTP_200_OK)

        if skills == 'all':
            return Response({'data': self.get_all_products_with_skill(specific_vendor=vendors_list)},
                            status=status.HTTP_200_OK)


        return Response({'data':[]},status=status.HTTP_400_BAD_REQUEST)









        






