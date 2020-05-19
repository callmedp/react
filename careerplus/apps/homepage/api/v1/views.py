import logging
from rest_framework.generics import RetrieveAPIView ,ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from shared.rest_addons.mixins import FieldFilterMixin
from django.template.loader import get_template

from weasyprint import HTML
from django.template import Context

import datetime
from django.utils import timezone

from .serializers import StaticSiteContentSerializer, OrderItemDetailSerializer, DashboardCancellationSerializer

from core.library.gcloud.custom_cloud_storage import \
    GCPPrivateMediaStorage, GCPInvoiceStorage, GCPMediaStorage, GCPResumeBuilderStorage
from wsgiref.util import FileWrapper
from django.conf import settings
import mimetypes




from homepage.models import StaticSiteContent,TestimonialCategoryRelationship,Testimonial
from shop.models import Category
from order.models import Order, OrderItem ,InternationalProfileCredential
from dashboard.dashboard_mixin import DashboardInfo, DashboardCancelOrderMixin
from core.api_mixin import ShineCandidateDetail
from django.core.files.base import ContentFile


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
        category_ids = eval(request.POST.get('categories','[]'))
        if not category_ids:
            return HttpResponse("No Changes")
        testimonial_id = request.POST.get('testimonial','')
        prev_category_mapping_ids = set(TestimonialCategoryRelationship.objects.\
            filter(testimonial=testimonial_id).values_list('category',flat=True))
        category_ids = set(category_ids)
        # mapping testimonial to category ids and delete some relations
        category_ids_to_delete = prev_category_mapping_ids - category_ids
        category_ids_to_add = category_ids - prev_category_mapping_ids 
        categories = Category.objects.filter(id__in=category_ids_to_add).only('id')
        testimonial = Testimonial.objects.filter(id=testimonial_id).first()

        if not testimonial:
            return HttpResponse("Failed")

        if category_ids_to_delete:
            TestimonialCategoryRelationship.objects.filter(category__in=category_ids_to_delete,testimonial=testimonial_id).delete()

        for category in categories:
            TestimonialCategoryRelationship.objects.get_or_create(category=category,testimonial=testimonial)

        return HttpResponse("Successful")


class UserDashboardApi(FieldFilterMixin, ListAPIView):
    """
     This api gives all the the order items.
    """
    # authentication_classes = (IsAuthenticated)
    permission_classes = ()
    authentication_classes = ()
    serializer_class = OrderItemDetailSerializer

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
            days = 18*30
            select_type = 0

        last_payment_date = timezone.now() - datetime.timedelta(days=days)
        queryset_list = OrderItem.objects.filter(no_process=False, order__site=2,
                                                 product__type_flow__in=[1, 12, 13, 4, 5, 8])

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
                                                 order__site=2)

            return queryset_list


class DashboardDetailApi(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = None

    def get(self, request):
        candidate_id = request.GET.get('candidate_id', '')
        orderitem_id = request.GET.get('orderitem_id')

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
            logger.error('OrderItem for candidate_id %s and pk %s with order status in [1, 3] does not exist' %(
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

        # ops = ops.values_list('id', 'oi_status', 'draft_counter', 'get_user_oi_status', 'created__date',
        #
        #                       'oi_draft__name')
        ops = [{"id" : op.id, "oi_status" : op.oi_status, "draft_counter" : op.draft_counter,
                "get_user_oi_status" : op.get_user_oi_status, "created__date" : op.created.strftime("%b %d, ""%Y"),
                "oi_draft__name" : op.oi_draft.name if op.oi_draft else ""
                } for op in ops]


        resp_dict = {'status': 'Success', 'error': None, 'data': {'oi': {
            'oi_status': order_item.oi_status,
            'product_id': order_item.product_id,
            'product_type_flow': order_item.product.type_flow,
            'oi_resume': order_item.oi_resume.url,
            'product_sub_type_flow': order_item.product.sub_type_flow,
            'custom_operations': list(order_item.get_item_operations().values() if order_item.get_item_operations()
            else ''),
            'order_id': order_item.order_id,
            'oi_id': order_item.pk,
            'order_number': order_item.order.number,
            'product_name': order_item.product.get_name,
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
                                                                            email=email).filter(order__site=2)

            pending_resume_items = [{'id':oi.id,'product_name':oi.product.get_name if oi.product else ''
                                     ,'product_get_exp_db':oi.product.get_exp_db() if oi.product else ''
                                     } for oi in
                                    pending_resume_items]
            res = ShineCandidateDetail().get_candidate_detail(email=None, shine_id=candidate_id)
            resumes = res['resumes']
            default_resumes = [resume for resume in resumes if resume['is_default']][0]
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
        serializer = DashboardCancellationSerializer(request.data)
        if serializer.is_valid():
            candidate_id = serializer.data.get('candidate_id')
            email = serializer.data.get('email')
            order_id = serializer.data.get('order_id')
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return Response({'status': 'Failure', 'error': 'Order not found against id'},
                                status=status.HTTP_417_EXPECTATION_FAILED)
            try:
                cancellation = DashboardCancelOrderMixin().perform_cancellation(candidate_id=candidate_id, email=email,
                                                                                order=order)
            except Exception as exc:
                logger.error('Dashboard cancellation error %s' % exc)
                return Response({'status': 'Failure', 'error': exc}, status=status.HTTP_417_EXPECTATION_FAILED)
            if cancellation:
                return Response({'status': 'Success', 'error': None, 'cancelled': True}, status=status.HTTP_200_OK)
            return Response({'status': 'Failure', 'error': None, 'cancelled': False},
                            status=status.HTTP_417_EXPECTATION_FAILED)
        return Response(serializer.errors, status=status.HTTP_200_OK)

class OrderItemCommentApi(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None


    def get(self,request):
        candidate_id = request.GET.get('candidate_id')
        oi_pk = request.GET.get('oi_pk')

        if not oi_pk or not candidate_id:
            return Response({'error' : "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            oi = OrderItem.objects.get(id=oi_pk)
        except:
            return Response({'error':'ITEM NOT FOUND'},status=status.HTTP_400_BAD_REQUEST)
        if not oi.order.candidate_id == candidate_id or not oi.order.status in [1, 3]:
            return Response({'error' : "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

        message = oi.message_set.filter(is_internal=False).order_by('created')

        message = [{'added_by':msg.added_by.name if msg.added_by else '','message':msg.message,
                    'created':msg.created.strftime("%b %d,%Y"),
                    'candidate_id':msg.candidate_id
                    } for msg in message]

        data = {
            'oi_id':oi.id,
            'comment':message
        }

        return Response(data,status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):

        candidate_id =  request.data.get('candidate_id')
        oi_pk = request.data.get('oi_pk')
        comment = request.data.get('comment', '').strip()
        if not oi_pk or not candidate_id or not comment :
            return Response({'error':"BAD REQUEST"},status=status.HTTP_400_BAD_REQUEST)

        try:
            oi=OrderItem.objects.get(id=oi_pk)
        except:
            return Response({'error':'ITEM NOT FOUND'},status=status.HTTP_400_BAD_REQUEST)

        if oi.order.candidate_id != candidate_id:
            return Response({'error':'Un Authorized Access'},status=status.HTTP_401_UNAUTHORIZED)

        oi.message_set.create(
            message=comment,
            candidate_id=candidate_id,
        )
        message = oi.message_set.filter(is_internal=False).order_by('created')

        message = [{'added_by' : msg.added_by.name if msg.added_by else '', 'message' : msg.message,
                    'created' : msg.created.strftime("%b %d,%Y"),
                    'candidate_id' : msg.candidate_id
                    } for msg in message]

        data = {
            'oi_id' : oi.id,
            'comment' : message
        }

        return Response(data,status=status.HTTP_200_OK)


class DashboardResumeUploadApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes =None

    def post(self,request,*args,**kwargs):
        candidate_id = request.POST.get('candidate_id')
        if not candidate_id:
            return Response({'error': 'No credential Provided'},status=status.HTTP_401_UNAUTHORIZED)
        file = request.FILES.get('file', '')
        list_ids = request.POST.getlist('resume_pending', [])

        shine_resume = request.POST.get('shine_resume', None)
        if shine_resume:
            data = DashboardInfo().get_user_shine_resume(candidate_id=candidate_id)
            if data:
                response = ShineCandidateDetail().get_shine_candidate_resume(
                    candidate_id=candidate_id,
                    resume_id=data.get('resume_id'))

                if response.status_code == 200:
                    file = ContentFile(response.content)
                    data = {
                        "list_ids" : list_ids,
                        "candidate_resume" : file,
                        'last_oi_status' : 13,
                        'is_shine' : True,
                        'extension' : request.session.get('resume_extn', '')
                    }
                    DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)

                    return Response({'success':'resumeUpload'},status=status.HTTP_200_OK)
        else:

            if not file:
                return Response({'error':'No file found'},status=status.HTTP_400_BAD_REQUEST)
            extn = file.name.split('.')[-1]
            if extn in ['doc', 'docx', 'pdf'] and list_ids:
                data = {
                    "list_ids": list_ids,
                    "candidate_resume": file,
                    'last_oi_status': 3
                }
                DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)
                return Response({'success':'resumeuploaded'},status=status.HTTP_200_OK)


class DashboardResumeDownloadApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes = None

    def get(self, request, *args, **kwargs) :

        candidate_id = request.GET.get('candidate_id', None)
        order_pk = request.GET.get('order_pk',None)
        if not candidate_id or not order_pk:
            return Response({'error':'BAD REQUEST'},status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(pk=order_pk)
        except:
            logging.getLogger('error_log').error('no order found {}'.format(order_pk))
            return Response({'error':'Order not Found'},status=status.HTTP_400_BAD_REQUEST)


        if not order.candidate_id == candidate_id:
            return Response({'error':'Unauthorized request'},status=status.HTTP_401_UNAUTHORIZED)

        if order.status in [1, 3]:
            file = request.GET.get('path', None)
            if not file:
                return Response({'error': 'file not found'}, status=status.HTTP_200_OK)

            if file.startswith('/'):
                file = file[1:]
            file_path = settings.RESUME_DIR + file
            try:
                if not settings.IS_GCP :
                    fsock = FileWrapper(open(file_path, 'rb'))
                else :
                    fsock = GCPPrivateMediaStorage().open(file_path)
            except:
                return Response({'error': 'file not found'}, status=status.HTTP_200_OK)

            filename = file.split('/')[-1]
            response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response
        else:
            return Response({'error':'Unauthorized request'},status=status.HTTP_401_UNAUTHORIZED)

class DashboardDraftDownloadApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes =None

    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id', None)
        orderitem_id = request.GET.get('oi_pk',None)
        if not candidate_id or not orderitem_id:
            return Response({'error':'BAD REQUEST'},status=status.HTTP_400_BAD_REQUEST)
        try:
            order_item = OrderItem.objects.get(pk=orderitem_id)
        except:
            logging.getLogger('error_log').error('no orderitem found {}'.format(orderitem_id))
            return Response({'error':'Order not Found'},status=status.HTTP_400_BAD_REQUEST)

        if not order_item.order.candidate_id == candidate_id:
            return Response({'error':'Unauthorized request'},status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({'error':'somewthing went wrong'},status=status.HTTP_400_BAD_REQUEST)

class ResumeProfileCredentialDownload(APIView):

    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('candidate_id')
        oi = request.GET.get('oi')
        if not candidate_id or not oi:
            return Response({'error':'BAD REQUEST'},status=status.HTTP_400_BAD_REQUEST)
        try:
            oi = OrderItem.objects.select_related('order').get(pk=oi)
        except:
            logging.getLogger('error_log').error('order item not found for {}'.format(oi))
            return Response({'error':'BAD REQUEST'},status=status.HTTP_400_BAD_REQUEST)

        profile_credentials = InternationalProfileCredential.objects.filter(
            oi=oi)
        if not profile_credentials:
            return Response({'error' : 'BAD REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

        if oi.order.candidate_id != candidate_id:
            return Response({'error' : 'Unauthorized REQUEST'}, status=status.HTTP_401_UNAUTHORIZED)

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
        return Response({'error':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)

