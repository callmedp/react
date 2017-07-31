import datetime

from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.middleware.csrf import get_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from order.models import Order, OrderItem


class DashboardInfo(object):
    def get_inbox_list(self, candidate_id=None, request=None, last_month_from=3, select_type=0, page=1):
        if candidate_id:
            days = last_month_from * 30
            last_payment_date = timezone.now() - datetime.timedelta(days=days)
            orderitems = OrderItem.objects.filter(
                order__status__in=[1, 3],
                order__candidate_id=candidate_id,
                order__payment_date__gte=last_payment_date, no_process=False)
            # if active:
            #     orderitems = orderitems.exclude(oi_status=4)
            # else:
            #     orderitems = orderitems.filter(oi_status=4)

            orderitems = orderitems.select_related(
                'order', 'product', 'partner')
            paginator = Paginator(orderitems, 2)
            try:
                orderitems = paginator.page(page)
            except PageNotAnInteger:
                orderitems = paginator.page(1)
            except EmptyPage:
                orderitems = paginator.page(paginator.num_pages)
            data = {
                "orderitems": orderitems,
                "max_draft_limit": settings.DRAFT_MAX_LIMIT,
                "csrf_token_value": get_token(request),
                "last_month_from": last_month_from,
                "select_type": select_type,
            }
            return render_to_string('partial/user-inboxlist.html', data)

    def get_myorder_list(self, candidate_id=None):
        if candidate_id:
            days = 3 * 30
            last_dateplaced_date = timezone.now() - datetime.timedelta(days=days)
            orders = Order.objects.filter(
                status__in=[1, 2, 3],
                candidate_id=candidate_id,
                date_placed__gte=last_dateplaced_date)

            order_list = []
            for obj in orders:
                orderitems = obj.orderitems.filter(no_process=False)
                orderitems.select_related('product')
                item_count = orderitems.count()
                data = {
                    "order": obj,
                    "item_count": item_count,
                    "orderitems": orderitems,
                }
                order_list.append(data)

            context = {
                "order_list": order_list,
            }
            return render_to_string('partial/myorder-list.html', context)

    # def get_inbox_oi_detail(self, candidate_id=None, oi=None):
    #     if oi and oi.order.candidate_id == candidate_id:
    #         if oi.product.type_flow in [1, 12, 13]:
    #             ops = oi.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 24, 26, 27])

    #         if ops.exists():
    #             data = {
    #                 "oi": oi,
    #                 "ops": ops,
    #                 "max_draft_limit": settings.DRAFT_MAX_LIMIT,
    #             }
    #             return render_to_string('include/inboxoi-deatil.html', data)

    def get_pending_resume_items(self, candidate_id=None, email=None):
        if candidate_id:
            resume_pending_items = OrderItem.objects.filter(order__candidate_id=candidate_id, order__status__in=[1, 3], no_process=False, oi_status=2)

        elif email:
            resume_pending_items = OrderItem.objects.filter(order__email=email, order__status__in=[1, 3], no_process=False, oi_status=2)

        return resume_pending_items.select_related('order', 'partner', 'product')

    def upload_candidate_resume(self, candidate_id=None, data={}):
        if candidate_id:
            file = data.get('candidate_resume', '')
            list_ids = data.get('list_ids', [])
            if file and list_ids:
                pending_resumes = OrderItem.objects.filter(id__in=list_ids, order__candidate_id=candidate_id, no_process=False, oi_status=2)
                for obj in pending_resumes:
                    obj.oi_resume = file
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
