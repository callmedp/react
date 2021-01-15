# Python Core Import
import logging, json
import datetime
import mimetypes
import random

# DRF Import
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

# Core Django Import
from django.http import HttpResponse, HttpResponsePermanentRedirect
from shared.rest_addons.mixins import FieldFilterMixin
from shared.rest_addons.pagination import LearningCustomPagination
from django.template.loader import get_template
from django.utils import timezone
from django.conf import settings
from django.db.models import Count, F, Prefetch, Value, CharField
from haystack.query import SearchQuerySet
from django.core.cache import cache
from django.db.models.functions import Concat

# Local Import
from core.mixins import InvoiceGenerate
from review.models import Review
from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from django.contrib.contenttypes.models import ContentType
from order.api.v1.serializers import OrderItemSerializer
from .serializers import StaticSiteContentSerializer, OrderItemDetailSerializer, DashboardCancellationSerializer,ProductSerializer
from core.library.gcloud.custom_cloud_storage import \
    GCPPrivateMediaStorage, GCPInvoiceStorage, GCPMediaStorage, GCPResumeBuilderStorage

# Local Inter App Import
from homepage.models import StaticSiteContent, TestimonialCategoryRelationship, Testimonial, \
    TopTrending, TrendingProduct, HomePageOffer, NavigationSpecialTag
from shop.models import Category, Product, ProductSkill, ProductCategory
from order.models import Order, OrderItem, InternationalProfileCredential
from dashboard.dashboard_mixin import DashboardInfo, DashboardCancelOrderMixin
from core.api_mixin import ShineCandidateDetail
from django.core.files.base import ContentFile
from payment.models import PaymentTxn
from .helper import APIResponse
from .serializers import RecentCourseSerializer
from .mixins import PopularProductMixin

# Other Import
from weasyprint import HTML
from wsgiref.util import FileWrapper

logger = logging.getLogger('error_log')


class StaticSiteView(RetrieveAPIView):
    # queryset = TermAndAgreement.objects.all()
    serializer_class = StaticSiteContentSerializer
    authentication_classes = ()
    permission_classes = ()
    lookup_field = 'page_type'

    def get_queryset(self):
        page_type = int(self.kwargs['page_type'])
        if page_type:
            return StaticSiteContent.objects.filter(page_type=page_type)
        return StaticSiteContent.objects.all()


class TestimonialCategoryMapping(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        category_ids = eval(request.POST.get('categories', '[]'))
        if not category_ids:
            return HttpResponse("No Changes")
        testimonial_id = request.POST.get('testimonial', '')
        prev_category_mapping_ids = set(TestimonialCategoryRelationship.objects. \
                                        filter(testimonial=testimonial_id).values_list('category', flat=True))
        category_ids = set(category_ids)
        # mapping testimonial to category ids and delete some relations
        category_ids_to_delete = prev_category_mapping_ids - category_ids
        category_ids_to_add = category_ids - prev_category_mapping_ids
        categories = Category.objects.filter(id__in=category_ids_to_add).only('id')
        testimonial = Testimonial.objects.filter(id=testimonial_id).first()

        if not testimonial:
            return HttpResponse("Failed")

        if category_ids_to_delete:
            TestimonialCategoryRelationship.objects.filter(category__in=category_ids_to_delete,
                                                           testimonial=testimonial_id).delete()

        for category in categories:
            TestimonialCategoryRelationship.objects.get_or_create(category=category, testimonial=testimonial)

        return HttpResponse("Successful")


class UserDashboardApi(FieldFilterMixin, ListAPIView):
    """
     This api gives all the the order items.
    """
    # authentication_classes = (IsAuthenticated)
    permission_classes = ()
    authentication_classes = ()
    serializer_class = OrderItemDetailSerializer
    pagination_class = LearningCustomPagination

    def get_queryset(self, *args, **kwargs):
        email = self.request.GET.get("email", None)
        candidate_id = self.request.GET.get("candidate_id", None)
        select_type = self.request.GET.get("select_type", 0)
        days = 0
        last_month_from = self.request.GET.get("last_month_from", 18)
        try:
            days = int(last_month_from) * 30
            select_type = int(select_type)
        except:
            days = 18 * 30
            select_type = 0

        last_payment_date = timezone.now() - datetime.timedelta(days=days)
        queryset_list = OrderItem.objects.filter(no_process=False)

        if select_type == 1:
            queryset_list = queryset_list.exclude(oi_status=4)
        elif select_type == 2:
            queryset_list = queryset_list.filter(oi_status=4)

        if not email and not candidate_id:
            return queryset_list.none()

        queryset_list = queryset_list.prefetch_related('product', 'product__product_class', 'delivery_service',
                                                       'order', 'product__attributes'
                                                       ).order_by('-order__payment_date')

        if candidate_id and not email:
            return queryset_list.filter(order__candidate_id=candidate_id, order__status__in=[1, 3],
                                        order__payment_date__gte=last_payment_date)

        if email and not candidate_id:
            return queryset_list.filter(order__email=email, order__payment_date__gte=last_payment_date,
                                        order__status__in=[1, 3])

        if email and candidate_id:
            queryset_list = queryset_list.filter(order__candidate_id=candidate_id, order__status__in=[1, 3],
                                                 order__payment_date__gte=last_payment_date)
            if not queryset_list.exists():
                queryset_list = queryset_list.filter(order__email=email, order__status__in=[1, 3])

            queryset_list = queryset_list.filter(order__email=email, order__status__in=[1, 3], no_process=False,
                                                 )
            return queryset_list


class DashboardDetailApi(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = None

    def get(self, request):
        candidate_id = request.GET.get('candidate_id', '')
        orderitem_id = request.GET.get('orderitem_id')
        # import ipdb;ipdb.set_trace()
        if not candidate_id:
            return Response({'status': 'Failure', 'error': 'candidate_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not orderitem_id:
            return Response({'status': 'Failure', 'error': 'orderitem_id is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            order_item = OrderItem.objects.select_related('order', 'product').get(
                pk=orderitem_id, order__candidate_id=candidate_id, order__status__in=[1, 3])
        except OrderItem.DoesNotExist:
            logger.error('OrderItem for candidate_id %s and pk %s with order status in [1, 3] does not exist' % (
                candidate_id, orderitem_id))
            return Response({'status': 'Failure', 'error': 'OrderItem does not exists.'})

        ops = []

        if order_item.product.type_flow in [1, 12, 13]:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163, 164, 181])

        elif order_item.product.vendor.slug == 'neo':
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 33, 4, 161, 162, 163, 164])

        elif order_item.product.type_flow in [2, 14]:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163, 164])

        elif order_item.product.type_flow == 3:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163, 164])
        elif order_item.product.type_flow == 4:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
        elif order_item.product.type_flow == 5:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
        elif order_item.product.type_flow == 6:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163, 164])
        elif order_item.product.type_flow in [7, 15]:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 6, 61, 161, 162, 163, 164])
        elif order_item.product.type_flow == 8:
            oi_status_list = [2, 49, 5, 46, 48, 27, 4, 161, 162, 163, 181, 164]
            ops = order_item.orderitemoperation_set.filter(oi_status__in=oi_status_list)
        elif order_item.product.type_flow == 10:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163, 164])
        elif order_item.product.type_flow == 16:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[5, 6, 4])
        elif order_item.product.type_flow == 17:
            ops = order_item.orderitemoperation_set.filter(oi_status__in=[0])

        # ops = ops.values_list('id', 'oi_status', 'draft_counter', 'get_user_oi_status', 'created__date',
        #
        #                       'oi_draft__name')
        ops = [{"id": op.id, "oi_status": op.oi_status, "draft_counter": op.draft_counter,
                "get_user_oi_status": op.get_user_oi_status, "created__date": op.created.strftime("%b %d, ""%Y"),
                "oi_draft__name": op.oi_draft.name if op.oi_draft else ""
                } for op in ops]

        resp_dict = {'status': 'Success', 'error': None, 'data': {'oi': {
            'oi_status': order_item.oi_status,
            'product_id': order_item.product_id,
            'product_type_flow': order_item.product.type_flow,
            'oi_resume': order_item.oi_resume.name if order_item.oi_resume else '',
            'product_sub_type_flow': order_item.product.sub_type_flow,
            'custom_operations': list(order_item.get_item_operations().values() if order_item.get_item_operations()
                                      else ''),
            'order_id': order_item.order_id,
            'oi_id': order_item.pk,
            'order_number': order_item.order.number if order_item.order_id else '',
            'product_name': order_item.product.get_name if order_item.product else '',
            'product_exp_db': order_item.product.get_exp_db(),
            'ops': ops,
        }}}

        return Response(resp_dict, status=status.HTTP_200_OK)


class DashboardNotificationBoxApi(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None

    def get(self, request):
        candidate_id = request.GET.get('candidate_id', None)
        email = request.GET.get('email', None)

        if not candidate_id:
            return Response({'status': 'Failure', 'error': 'candidate_id is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({'status': 'Failure', 'error': 'email is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # this is order__site=2 is required to get the data for resume.shine
            pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id,
                                                                            email=email)

            pending_resume_items = [{'id': oi.id, 'product_name': oi.product.get_name if oi.product else ''
                                        , 'product_get_exp_db': oi.product.get_exp_db() if oi.product else ''
                                     } for oi in
                                    pending_resume_items]
            res = ShineCandidateDetail().get_candidate_detail(email=None, shine_id=candidate_id)
            resumes = res['resumes']
            default_resumes = [resume for resume in resumes if resume and resume['is_default']]
            if len(default_resumes):
                default_resumes = default_resumes[0]
            else:
                default_resumes = {}
        except Exception as exc:
            logger.error('Error in getting notifications %s' % exc)
            return Response({'status': 'Failure', 'error': 'Default resume does not exist'},
                            status=status.HTTP_417_EXPECTATION_FAILED)

        resp_dict = {'status': 'Success', 'error': None, 'data': {
            "resume_id": default_resumes.get('id', ''),
            "shine_resume_name": default_resumes.get('resume_name', ''),
            "resume_extn": default_resumes.get('extension', ''),
            "pending_resume_items": list(pending_resume_items)
        }}

        return Response(resp_dict, status=status.HTTP_200_OK)


class DashboardCancellationApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = DashboardCancellationSerializer

    def post(self, request):
        serializer = DashboardCancellationSerializer(data=request.data)
        if serializer.is_valid():
            candidate_id = serializer.data.get('candidate_id')
            email = serializer.data.get('email')
            order_id = serializer.data.get('order_id')
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return Response({'status': 'Failure', 'error': 'Order not found against id'},
                                status=status.HTTP_417_EXPECTATION_FAILED)

            if order.candidate_id != candidate_id:
                return Response({'status': 'Failure', 'error': 'Order not found against id'},
                                status=status.HTTP_417_EXPECTATION_FAILED)
            try:
                cancellation = DashboardCancelOrderMixin().perform_cancellation(candidate_id=candidate_id, email=email,
                                                                                order=order)
            except Exception as exc:
                logger.error('Dashboard cancellation error %s' % exc)
                return Response({'status': 'Failure', 'error': exc}, status=status.HTTP_417_EXPECTATION_FAILED)
            if cancellation:
                return Response({'status': 'Success', 'data': order_id, 'error': None, 'cancelled': True},
                                status=status.HTTP_200_OK)
            return Response({'status': 'Failure', 'error': None, 'cancelled': False},
                            status=status.HTTP_417_EXPECTATION_FAILED)
        return Response(serializer.errors, status=status.HTTP_200_OK)


class OrderItemCommentApi(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None

    def get(self, request):
        candidate_id = request.GET.get('candidate_id')
        oi_pk = request.GET.get('oi_pk')

        if not oi_pk or not candidate_id:
            return Response({'error': "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            oi = OrderItem.objects.get(id=oi_pk)
        except:
            return Response({'error': 'ITEM NOT FOUND'}, status=status.HTTP_400_BAD_REQUEST)
        if not oi.order.candidate_id == candidate_id or not oi.order.status in [1, 3]:
            return Response({'error': "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

        message = oi.message_set.filter(is_internal=False).order_by('created')

        message = [{'added_by': msg.added_by.name if msg.added_by else '', 'message': msg.message,
                    'created': msg.created.strftime("%b %d,%Y"),
                    'candidate_id': msg.candidate_id
                    } for msg in message]

        data = {
            'oi_id': oi.id,
            'comment': message
        }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        candidate_id = request.data.get('candidate_id')
        oi_pk = request.data.get('oi_pk')
        comment = request.data.get('comment', '').strip()
        if not oi_pk or not candidate_id or not comment:
            return Response({'error': "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            oi = OrderItem.objects.get(id=oi_pk)
        except:
            return Response({'error': 'ITEM NOT FOUND'}, status=status.HTTP_400_BAD_REQUEST)

        if oi.order.candidate_id != candidate_id:
            return Response({'error': 'Un Authorized Access'}, status=status.HTTP_401_UNAUTHORIZED)

        oi.message_set.create(
            message=comment,
            candidate_id=candidate_id,
        )
        message = oi.message_set.filter(is_internal=False).order_by('created')

        message = [{'added_by': msg.added_by.name if msg.added_by else '', 'message': msg.message,
                    'created': msg.created.strftime("%b %d,%Y"),
                    'candidate_id': msg.candidate_id
                    } for msg in message]

        data = {
            'oi_id': oi.id,
            'comment': message
        }

        return Response(data, status=status.HTTP_200_OK)


class DashboardResumeUploadApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes = None

    def post(self, request, *args, **kwargs):
        candidate_id = request.POST.get('candidate_id')
        if not candidate_id:
            return Response({'error': 'No credential Provided'}, status=status.HTTP_401_UNAUTHORIZED)
        file = request.FILES.get('file', '')
        list_ids = request.POST.get('resume_pending', '')
        list_ids = list_ids.split(',')

        shine_resume = request.POST.get('resume_shine', None)
        if shine_resume:
            data = DashboardInfo().get_user_shine_resume(candidate_id=candidate_id)
            if data:
                response = ShineCandidateDetail().get_shine_candidate_resume(
                    candidate_id=candidate_id,
                    resume_id=data.get('resume_id'))

                if response.status_code == 200:
                    file = ContentFile(response.content)
                    data = {
                        "list_ids": list_ids,
                        "candidate_resume": file,
                        'last_oi_status': 13,
                        'is_shine': True,
                        'extension': request.session.get('resume_extn', '')
                    }

                    DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

                    return Response({'success': 'resumeUpload'}, status=status.HTTP_200_OK)

            return Response({'error': 'Something went Wrong'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not file:
                return Response({'error': 'No file found'}, status=status.HTTP_400_BAD_REQUEST)
            extn = file.name.split('.')[-1]
            if extn in ['doc', 'docx', 'pdf'] and list_ids:
                data = {
                    "list_ids": list_ids,
                    "candidate_resume": file,
                    'last_oi_status': 3
                }
                try:
                    DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)
                except:
                    return Response({'error': 'Something went Wrong'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'success': 'resumeuploaded'}, status=status.HTTP_200_OK)
            return Response({'error': 'Something went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


class DashboardResumeDownloadApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes = None

    def get(self, request, *args, **kwargs):

        candidate_id = request.GET.get('candidate_id', None)
        order_pk = request.GET.get('order_pk', None)
        if not candidate_id or not order_pk:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))
        try:
            order = Order.objects.get(pk=order_pk)
        except:
            logging.getLogger('error_log').error('no order found {}'.format(order_pk))
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

        if not order.candidate_id == candidate_id:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

        if order.status in [1, 3]:
            file = request.GET.get('path', None)
            if not file:
                return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

            if file.startswith('/'):
                file = file[1:]
            file_path = settings.RESUME_DIR + file
            try:
                if not settings.IS_GCP:
                    fsock = FileWrapper(open(file_path, 'rb'))
                else:
                    fsock = GCPPrivateMediaStorage().open(file_path)
            except:
                return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

            filename = file.split('/')[-1]
            response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response
        else:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))


class DashboardDraftDownloadApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes = None

    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id', None)
        orderitem_id = request.GET.get('oi_pk', None)
        if not candidate_id or not orderitem_id:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))
        try:
            order_item = OrderItem.objects.get(pk=orderitem_id)
        except:
            logging.getLogger('error_log').error('no orderitem found {}'.format(orderitem_id))
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

        if not order_item.order.candidate_id == candidate_id:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))
        try:
            flag2 = False
            draft = order_item.oio_linkedin
            name = draft.candidate_name
            skill_list = draft.key_skills
            organization_list = draft.from_organization.filter(org_current=False).order_by('-work_to')
            education_list = draft.from_education.filter(edu_current=False).order_by('-study_to')
            current_org = draft.from_organization.filter(org_current=True)
            current_edu = draft.from_education.filter(edu_current=True)
            if current_edu:
                current_edu = current_edu[0]
            if current_org:
                current_org = current_org[0]
            if draft.profile_photo:
                flag2 = True
            if draft.public_url:
                flag2 = True
            if draft.recommendation:
                flag2 - True
            if draft.follow_company:
                flag2 = True
            if draft.join_group:
                flag2 = True

            context_dict = {
                'pagesize': 'A4',
                'orderitem': order_item,
                'draft': draft,
                'name': name,
                'skill_list': skill_list.split(','),
                'organization_list': organization_list,
                'education_list': education_list,
                'flag2': flag2,
                'current_edu': current_edu,
                'current_org': current_org,
            }
            template = get_template('linkedin/linkedin-resume-pdf.html')
            html = template.render(context_dict)
            pdf_file = HTML(string=html).write_pdf()
            http_response = HttpResponse(pdf_file, content_type='application/pdf')
            http_response['Content-Disposition'] = 'filename="linkedin-draft.pdf"'
            return http_response
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))


class ResumeProfileCredentialDownload(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes = None

    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id')
        oi = request.GET.get('oi')
        if not candidate_id or not oi:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))
        try:
            oi = OrderItem.objects.select_related('order').get(pk=oi)
        except:
            logging.getLogger('error_log').error('order item not found for {}'.format(oi))
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

        profile_credentials = InternationalProfileCredential.objects.filter(
            oi=oi)
        if not profile_credentials:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

        if oi.order.candidate_id != candidate_id:
            return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))

        if profile_credentials:
            try:
                context_dict = {
                    'pagesize': 'A4',
                    'profile_credentials': profile_credentials,
                }
                template = get_template('console/order/profile-update-credentials.html')
                html = template.render(context_dict)
                pdf_file = HTML(string=html).write_pdf()
                http_response = HttpResponse(pdf_file, content_type='application/pdf')
                http_response['Content-Disposition'] = 'filename="profile_credential.pdf"'
                return http_response
            except Exception as e:
                logging.getLogger('error_log').error(
                    "Profile download:%s", str(e))
        return HttpResponsePermanentRedirect('{}/404'.format(settings.RESUME_SHINE_MAIN_DOMAIN))


class UserInboxListApiView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id')
        if not candidate_id:
            return Response({'error': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(
            status__in=[0, 1, 3],
            candidate_id=candidate_id)

        excl_txns = PaymentTxn.objects.filter(
            status__in=[0, 2, 3, 4, 5],
            payment_mode__in=[6, 7],
            order__candidate_id=candidate_id)

        excl_order_list = excl_txns.all().values_list('order_id', flat=True)
        orders = orders.exclude(id__in=excl_order_list).order_by('-date_placed')
        order_list = []
        for obj in orders:
            orderitems = OrderItem.objects.prefetch_related('product', 'product__product_class', 'parent').filter(
                no_process=False, order=obj)
            product_type_flow = None
            product_id = None
            item_count = len(orderitems)
            if item_count > 0:
                item_order = orderitems[0]
                product_type_flow = item_order and item_order.product_id and item_order.product.type_flow or 0
                product_id = item_order and item_order.product_id

            data = {
                "item_count": item_count,
                "get_currency": obj.get_currency(),
                'total_incl_tax': obj.total_incl_tax,
                'number': obj.number, 'date_placed': obj.date_placed.strftime("%b %d, ""%Y"),
                'status': obj.status, 'id': obj.id,
                'orderitems': [{'product_type_flow': oi.product.type_flow if oi.product_id else '',
                                'parent': oi.parent_id,
                                'parent_heading': oi.parent.product.heading if oi.parent_id and oi.parent.product_id else '',
                                'get_user_oi_status': oi.get_user_oi_status,
                                'heading': oi.product.heading if oi.product_id else '',
                                'get_name': oi.product.get_name if oi.product_id else '',
                                'get_exp_db': oi.product.get_exp_db() if oi.product_id else '',
                                'get_studymode_db': '',
                                'get_coursetype_db': '',
                                'get_duration_in_day': oi.product.get_duration_in_ddmmyy() if oi.product_id and
                                                                                              oi.product.get_duration_in_day() else '',
                                'oi_status': oi.oi_status, } for oi in orderitems]
            }
            order_list.append(data)

        return Response({'data': order_list}, status=status.HTTP_200_OK)


class DashboardResumeInvoiceDownload(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id', None)
        email = request.GET.get('email', None)
        order_pk = request.GET.get('order_pk', None)
        try:
            order = Order.objects.get(pk=order_pk)

            if candidate_id and order.status in [1, 3] and (order.email == email or order.candidate_id == candidate_id):
                if order.invoice:
                    invoice = order.invoice
                else:
                    order, invoice = InvoiceGenerate().save_order_invoice_pdf(order=order)
                if invoice:
                    file_path = invoice.name
                    if not settings.IS_GCP:
                        file_path = invoice.path
                        fsock = FileWrapper(open(file_path, 'rb'))
                    else:
                        fsock = GCPInvoiceStorage().open(file_path)
                    filename = invoice.name.split('/')[-1]
                    response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
                    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
                    return response
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
        return Response({'error': 'Something Went Wrong'})


class DashboardFeedbackSubmit(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def post(self, request, *args, **kwargs):
        email_dict = {}
        candidate_id = request.data.get('candidate_id', None)
        oi_pk = request.data.get('oi_pk')
        email = request.data.get('email')
        data = {
            "display_message": 'Thank you for sharing your valuable feedback',
        }
        if oi_pk and candidate_id:
            try:
                oi = OrderItem.objects.select_related("order").get(id=oi_pk)
                review = request.data.get('review', '').strip()
                rating = int(request.data.get('rating', 1))
                title = request.data.get('title', '').strip()
                name = request.data.get('full_name')
                if rating and oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3]:
                    content_type = ContentType.objects.get(app_label="shop", model="product")
                    review_obj = Review.objects.create(
                        content_type=content_type,
                        object_id=oi.product_id,
                        user_name=name,
                        user_email=email,
                        user_id=candidate_id,
                        content=review,
                        average_rating=rating,
                        title=title
                    )

                    extra_content_obj = ContentType.objects.get(app_label="order", model="OrderItem")

                    review_obj.extra_content_type = extra_content_obj
                    review_obj.extra_object_id = oi.id
                    review_obj.save()

                    oi.user_feedback = True
                    oi.save()
                    # send mail for coupon
                    if oi.user_feedback:
                        mail_type = "FEEDBACK_COUPON"
                        to_emails = [oi.order.get_email()]
                        email_dict.update({
                            "username": oi.order.first_name if oi.order.first_name else oi.order.candidate_id,
                            "subject": 'You earned a discount coupon worth Rs. <500>',
                            "coupon_code": '',
                            'valid': '',
                        })

                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                else:
                    data['display_message'] = "select valid input for feedback"
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)


            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                data['display_message'] = "select valid input for feedback"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Something went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


class PausePlayService(UpdateAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = OrderItemSerializer
    queryset = OrderItem.objects.all()
    owner_fields = ['order.candidate_id']


class NeoBoardUserAPI(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def post(self, request, *args, **kwargs):
        from order.models import OrderItem
        from order.tasks import board_user_on_neo
        candidate_id = request.data.get('candidate_id')
        oi_pk = request.data.get('oi_pk')
        if not candidate_id:
            return Response({'error': 'candidate id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not oi_pk:
            return Response({'error': 'orderitem id is missing'}, status=status.HTTP_400_BAD_REQUEST)

        oi = OrderItem.objects.select_related("order").filter(pk=oi_pk).first()
        order = oi.order

        if oi and oi.product.vendor.slug == 'neo' and order.candidate_id == candidate_id and order.status in [1, 3]:
            if not oi.neo_mail_sent:
                boarding_type = board_user_on_neo([oi.id])
                msg = 'Please check you mail to confirm boarding on Neo'
                if boarding_type == 'already_trial':
                    msg = 'You Account has been Updated from Trial To Regular'
                return Response({'data': msg}, status=status.HTTP_200_OK)

        return Response({'data': ''}, status=status.HTTP_200_OK)


class TrendingCoursesAndSkillsAPI(PopularProductMixin, APIView):
    __author__ = 'Rahul'

    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        """
        Aim is to find out the trending courses accross the plateform
        Mixing is used to fetch trending course to algorithm,
        please check "PopularProductMixin" to understand the algorithm.
        """
        popular_course_quantity = int(request.GET.get('num_courses', 2))
        skill_category = request.GET.get('category_id', None)

        product_obj, product_converstion_ratio, product_revenue_per_mile = PopularProductMixin().\
                                                                            popular_courses_algorithm(
                                                                            quantity=popular_course_quantity,
                                                                            category=skill_category)

        if not product_obj:
            return APIResponse(message='No Product Object Found !', status=status.HTTP_200_OK,
                               error=False)

        product_pks = list(product_converstion_ratio) + list(product_revenue_per_mile)
        tprds = SearchQuerySet().filter(id__in=product_pks, pTP__in=[0, 1, 3]).exclude(
            id__in=settings.EXCLUDE_SEARCH_PRODUCTS
        )
        # p_skills = product_obj.filter(id__in=product_pks, categories__is_skill=True).distinct().exclude(
        #     categories__related_to__slug__isnull=True)
        
        p_skills = ProductCategory.objects.filter(product__id__in=product_pks,category__is_skill=True).exclude(
            category__related_to__slug__isnull=True)
        
        skills = []
        skills_ids = []

        for i in p_skills:
            if i.category.id not in skills_ids:
                skills_ids.append(i.category.id)
                skills.append({'id': i.category.id, 'skillName': i.category.name,
                           'skillUrl': i.category.get_absolute_url()})

        data = {
            'trendingCourses': [
                {'id': tprd.id, 'heading': tprd.pHd, 'name': tprd.pNm, 'url': tprd.pURL, 'img': tprd.pImg, \
                 'img_alt': tprd.pImA, 'rating': tprd.pARx, 'vendor': tprd.pPvn, 'stars': tprd.pStar,
                 'provider': tprd.pPvn \
                 } for tprd in tprds],
            'trendingSkills': skills
        }
        return APIResponse(message='Trending Course Loaded', data=data, status=status.HTTP_200_OK)


class NavigationTagsAndOffersAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, format=None):
        """
        This will fetch the active offer and two special tags
        from the console
        """

        active_offer = []
        data = {}
        special_links = cache.get('active_homepage_navlink_new', [])
        whatsapp_no = cache.get('whatsapp_visibility_class', {})
        if not settings.DEBUG and special_links:
            active_navlinks = special_links
        else:
            data_obj_list = list(NavigationSpecialTag().get_active_navlink())
            active_navlinks = NavigationSpecialTag().convert_data_in_list(data_obj_list[:2])
            cache.set('active_homepage_navlink_new', active_navlinks, 24 * 60 * 60)

        data.update({
            'navTags': active_navlinks,
            'navOffer': active_offer,
            'callUs': settings.GGN_CONTACT_FULL,
            'whatsappDict': {
                "prd_course_visibility": whatsapp_no.get('product-course-visibility', False),
                "prd_course_number": whatsapp_no.get('product-course-number'),
                "prd_service_visibility": whatsapp_no.get('product-service-visibility', False),
                "prd_service_number": whatsapp_no.get('product-service-number'),
                "course_skill_visibility": whatsapp_no.get('course-skill-visibility', False),
                "course_skill_number": whatsapp_no.get('course-skill-number'),
                "service_skill_visibility": whatsapp_no.get('service-skill-visibility', False),
                "service_skill_number": whatsapp_no.get('service-skill-number')
            }
        })
        return APIResponse(message='Navigations Tags and Offers details fetched', data=data, status=status.HTTP_200_OK)


class PopularServicesAPI(PopularProductMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        """
        According to the algorithm of popular Courses find out the
        trending services.
        For detail please check TrendingCourseAPI
        """
        quantity_to_display = int(request.GET.get('num_services', 6))

        # class fall into service category
        class_category = settings.SERVICE_SLUG + settings.WRITING_SLUG

        s_obj, s_ratio, s_revenue = PopularProductMixin(). \
            popular_courses_algorithm(class_category=class_category,
                                      quantity=quantity_to_display)

        service_pks = list(s_ratio) + list(s_revenue)
        tsrvcs = SearchQuerySet().filter(id__in=service_pks, pTP__in=[0, 1, 3]).exclude(
            id__in=settings.EXCLUDE_SEARCH_PRODUCTS
        )
        data = {
            'popularServices': [
                {'id': tsrvc.id, 'heading': tsrvc.pHd, 'name': tsrvc.pNm, 'url': tsrvc.pURL, 'img': tsrvc.pImg, \
                 'img_alt': tsrvc.pImA, 'description': tsrvc.pDscPt, 'rating': tsrvc.pARx, 'price': tsrvc.pPinb, 'vendor': tsrvc.pPvn, 'stars': tsrvc.pStar,
                 'provider': tsrvc.pPvn} for tsrvc in tsrvcs]
        }
        return APIResponse(message='Popular Services Loaded', data=data, status=status.HTTP_200_OK)


class RecentCoursesAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        """
        Function must return the recent added course in the
        system with the logic according to handled by serializer
        """
        quantity_to_display = int(request.GET.get('num_recent', 6))

        # class getting the recent_ids from serializer
        queryset = Product.objects.filter(product_class__slug__in=settings.COURSE_SLUG,
                                          active=True,
                                          is_indexed=True).order_by('-created')[:quantity_to_display]\
                                          .values_list('id', flat=True)

        trcntss = SearchQuerySet().filter(id__in=list(queryset), pTP__in=[0, 1, 3]).exclude(
            id__in=settings.EXCLUDE_SEARCH_PRODUCTS
        ).order_by('-pCD')

        data = {
            'recentCoursesList':
                [
                    {
                    'id': trcnts.id, 'heading': trcnts.pHd, 'name': trcnts.pNm, 'url': trcnts.pURL, 'imgUrl': trcnts.pImg, \
                     'imgAlt': trcnts.pImA, 'rating': trcnts.pARx, 'price': trcnts.pPinb, 'vendor': trcnts.pPvn,
                     'stars': trcnts.pStar,'provider': trcnts.pPvn
                     } for trcnts in trcntss
                ]
        }
        return APIResponse(message='Recent Course fetched', data=data, status=status.HTTP_200_OK)

class TrendingCategoriesApi(PopularProductMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        cached_data = cache.get('category_popular_courses')
        if not settings.DEBUG and cached_data:
            data = cached_data
        else:
            data = {
                'SnMCourseList': PopularProductMixin().get_products_json(PopularProductMixin().\
                                                        get_popular_courses(category=17,quantity=3).\
                                                            values_list('id',flat=True)),
                'ITCourseList': PopularProductMixin().get_products_json(PopularProductMixin().\
                                                        get_popular_courses(category=22,quantity=3).\
                                                            values_list('id',flat=True)),
                'BnFCourseList': PopularProductMixin().get_products_json(PopularProductMixin().\
                                                        get_popular_courses(category=20,quantity=3).\
                                                            values_list('id',flat=True)),
            }
            cache.set('category_popular_courses',data,86400)
        return Response(data=data, status=status.HTTP_200_OK)
        
