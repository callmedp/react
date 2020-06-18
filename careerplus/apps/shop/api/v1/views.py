# python imports
import logging

# django imports
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


# local imports
from .serializers import (
    ProductListSerializerForAuditHistory,
    ProductDetailSerializer,
    PracticeTestInfoCreateSerializer,
    UpdateProductScreenSkillSerializer,
    UpdateProductSkillSerializer)
from django.contrib.contenttypes.models import ContentType

from .tasks import delete_from_solr, update_practice_test_info
from ..choices import av_status_choices

# interapp imports
from shop.models import (Product, ProductScreen, PracticeTestInfo, 
                    Skill, FunctionalArea, AnalyticsVidhyaRecord)
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
from django.conf import settings


# 3rd party imports
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


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

class AnalyticsVidhyaEnrollment(APIView):
    '''
    document at : https://gitlab.analyticsvidhya.com/snippets/30#endpoints
    '''
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        '''
        enrollment for course 
        '''
        data = self.request.data
        email = data.get('email','')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        course_id = data.get('course_id', '')
        course_name = data.get('course_name', '')
        price = data.get('price', '')
        phone_number = data.get('phone', '')
        request_url = settings.ANALYTICS_VIDHYA_URL.get('enrollment','')
        try:
            response = requests.post(request_url, data)
            if response.status_code == 201:
                logging.getLogger('info_log').info('lead is created')
            else:
                logging.getLogger('info_log').info('Error in response')
                return Response({'status': 'Failure', "msg": "Error \
                    in lead enrollment API"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.getLogger('error_log').error(e)
            return Response({'status': 'Failure', "msg": "Error in lead enrollment \
                API"}, status=status.HTTP_400_BAD_REQUEST)
        res_json = response.json()
        course_id = res_json.get('course_id','')
        AV_id = res_json.get('id','')
        status = res_json.get('status','')

        if not av_status_choices.get(status):
            logging.getLogger('error_log').error('invalid enrollment status')
            return Response({'status': 'Failure', "msg": "Error in lead enrollment API:\
                invalid enrollment status"}, status=status.HTTP_400_BAD_REQUEST)

        if AnalyticsVidhyaRecord.objects.filter(AV_Id=AV_id).exists():
            logging.getLogger('info_log').info('lead already exists')
            return Response({'status': 'success', "msg": "lead \
                already exists"}, status=status.HTTP_200_OK)

        AV_details = {
            'AV_Id' : AV_id,
            'name' : '{} {}'.format(first_name, last_name),
            'email' : email,
            'phone' : phone_number,
            'status' : av_status_choices.get(status)
            }
        try: 
            AnalyticsVidhyaRecord.objects.create(**AV_details)
        except Exception as e:
            logging.getLogger('error_log').error(e)
            return Response({'status': 'Failure', "msg": "Error in Saving leads created from"},
                            status=status.HTTP_400_BAD_REQUEST)