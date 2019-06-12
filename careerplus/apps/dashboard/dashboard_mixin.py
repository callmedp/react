import datetime
import os
import logging

from random import random

from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.template.context import RequestContext
from django.middleware.csrf import get_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.api_mixin import ShineCandidateDetail
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from order.models import Order, OrderItem
from payment.models import PaymentTxn


class DashboardInfo(object):

    def check_empty_inbox(self, candidate_id=None):
        if candidate_id:
            days = 18 * 30
            last_payment_date = timezone.now() - datetime.timedelta(days=days)
            orderitems = OrderItem.objects.filter(
                order__status__in=[1, 3],
                order__candidate_id=candidate_id,
                order__payment_date__gte=last_payment_date, no_process=False)
            if orderitems.exists():
                return False
        return True

    def get_inbox_list(self, candidate_id=None, request=None, last_month_from=18, select_type=0, page=1):
        if candidate_id:
            days = last_month_from * 30
            last_payment_date = timezone.now() - datetime.timedelta(days=days)
            orderitems = OrderItem.objects.filter(
                order__status__in=[1, 3],
                order__candidate_id=candidate_id,
                order__payment_date__gte=last_payment_date, no_process=False)
            if select_type == 1:
                orderitems = orderitems.exclude(oi_status=4)
            elif select_type == 2:
                orderitems = orderitems.filter(oi_status=4)

            orderitems = orderitems.select_related(
                'order', 'product', 'partner').order_by('-order__payment_date')
            paginator = Paginator(orderitems, 10)
            try:
                orderitems = paginator.page(page)
            except PageNotAnInteger:
                orderitems = paginator.page(1)
            except EmptyPage:
                orderitems = paginator.page(paginator.num_pages)
            
            context = {
                "orderitems": orderitems,
                "max_draft_limit": settings.DRAFT_MAX_LIMIT,
                "csrf_token_value": get_token(request),
                "last_month_from": last_month_from,
                "select_type": select_type,
            }

            return render_to_string('partial/user-inboxlist.html',context)

    def get_myorder_list(self, candidate_id=None, request=None):
        if not candidate_id:
            return
        # days = 6 * 30
        # last_dateplaced_date = timezone.now() - datetime.timedelta(days=days)
        orders = Order.objects.filter(
            status__in=[0, 1, 3],
            candidate_id=candidate_id)

        excl_txns = PaymentTxn.objects.filter(
            status__in=[0, 2, 3, 4, 5],
            payment_mode__in=[6, 7],
            order__candidate_id=candidate_id)
        # excl_txns = PaymentTxn.objects.filter(status=0, ).exclude(payment_mode__in=[1, 4])
        excl_order_list = excl_txns.all().values_list('order__pk', flat=True)

        orders = orders.exclude(id__in=excl_order_list)

        orders = orders.order_by('-date_placed')
        order_list = []
        for obj in orders:
            orderitems = obj.orderitems.filter(no_process=False)
            orderitems.select_related('product')
            product_type_flow = None
            product_id = None
            item_count = orderitems.count()
            if item_count > 0:
                item_order = orderitems.first()
                product_type_flow = item_order and item_order.product and item_order.product.type_flow or 0
                product_id =item_order and item_order.product and item_order.product.id or None
            data = {
                "order": obj,
                "item_count": item_count,
                'product_type_flow': product_type_flow,
                "product_id": product_id,
                "orderitems": orderitems,
            }
            order_list.append(data)

        if request:
            csrf_token = get_token(request)
        else:
            csrf_token = get_token(self.request)

        context = {
            "order_list": order_list,
            "csrf_token": csrf_token,
        }
        if not order_list:
            return ''
        return render_to_string('partial/myorder-list.html', context)

    def get_pending_resume_items(self, candidate_id=None, email=None):
        if candidate_id:
            resume_pending_items = OrderItem.objects.filter(order__candidate_id=candidate_id, order__status__in=[1, 3],
                                                            no_process=False, oi_status=2)

        elif email:
            resume_pending_items = OrderItem.objects.filter(order__email=email, order__status__in=[1, 3],
                                                            no_process=False, oi_status=2)

        return resume_pending_items.select_related('order', 'partner', 'product')

    def upload_candidate_resume(self, candidate_id=None, data={}):
        if candidate_id:
            file = data.get('candidate_resume', '')
            list_ids = data.get('list_ids', [])
            if file and list_ids:
                pending_resumes = OrderItem.objects.filter(order__status=1, id__in=list_ids,
                                                           order__candidate_id=candidate_id, no_process=False,
                                                           oi_status=2)
                path_dict = {}
                for obj in pending_resumes:
                    try:
                        order = obj.order
                        if not path_dict.get(order.pk):
                            filename = os.path.splitext(file.name)
                            extention = filename[len(filename) - 1] if len(
                                filename) > 1 else ''
                            file_name = 'resumeupload_' + str(order.pk) + '_' + str(int(random() * 9999)) \
                                        + '_' + timezone.now().strftime('%Y%m%d') + extention
                            full_path = '%s/' % str(order.pk)
                            if not settings.IS_GCP:
                                if not os.path.exists(settings.RESUME_DIR + full_path):
                                    os.makedirs(settings.RESUME_DIR + full_path)
                                dest = open(
                                    settings.RESUME_DIR + full_path + file_name, 'wb')
                                for chunk in file.chunks():
                                    dest.write(chunk)
                                dest.close()
                            else:
                                GCPPrivateMediaStorage().save(settings.RESUME_DIR + full_path + file_name, file)
                            path_dict[order.pk] = full_path + file_name
                    except Exception as e:
                        logging.getLogger('error_log').error("%s-%s" % ('resume_upload', str(e)))
                        continue

                    obj.oi_resume = path_dict[order.pk]
                    last_oi_status = obj.oi_status
                    obj.oi_status = 5
                    obj.last_oi_status = 3
                    obj.save()
                    obj.orderitemoperation_set.create(
                        oi_status=3,
                        oi_resume=obj.oi_resume,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to)

                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to)

    def check_user_shine_resume(self, candidate_id=None, request=None):
        if not request:
            request = self.request
        if candidate_id and not request.session.get('resume_id', None):
            res = ShineCandidateDetail().get_candidate_detail(email=None, shine_id=candidate_id)
            resumes = res.get('resumes', [])
            default_resumes = [resume for resume in resumes if resume['is_default']]
            if default_resumes:
                request.session.update({
                    "resume_id": default_resumes[0].get('id', ''),
                    "shine_resume_name": default_resumes[0].get('resume_name', ''),
                    "resume_extn": default_resumes[0].get('extension', ''),
                })
