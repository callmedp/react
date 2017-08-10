from django.http import (
    HttpResponseRedirect,)
from django.views.generic import TemplateView
from django.conf import settings
from django.core.urlresolvers import reverse

from console.decorators import Decorate, mobile_page_only
from order.models import OrderItem


@Decorate(mobile_page_only(redirect_url='/dashboard/'))
class DashboardItemDetailView(TemplateView):
    template_name = 'dashboard/dashboard-itemdetail.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if self.candidate_id:
            self.oi_pk = request.GET.get('oi', None)
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    return super(DashboardItemDetailView, self).get(request, args, **kwargs)
            except:
                pass
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardItemDetailView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            ops = []
            if self.oi.product.type_flow in [1, 12, 13]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 24, 26, 27])
            elif self.oi.product.type_flow == 2:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6])

            elif self.oi.product.type_flow == 3:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 121])
            elif self.oi.product.type_flow == 4:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61])
            elif self.oi.product.type_flow == 5:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61])
            elif self.oi.product.type_flow == 6:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82])
            elif self.oi.product.type_flow == 7:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 61, 62])
            elif self.oi.product.type_flow == 8:
                oi_status_list = [49, 5, 46, 48, 27, 4]
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=oi_status_list)
            elif self.oi.product.type_flow == 10:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 101])
            context.update({
                "oi": self.oi,
                "max_draft_limit": settings.DRAFT_MAX_LIMIT,
                "ops": list(ops),
            })
        return context


class DashboardItemFeedbackView(TemplateView):
    template_name = 'dashboard/dashboard-itemfeedback.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if self.candidate_id:
            self.oi_pk = request.GET.get('oi', None)
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3] and self.oi.oi_status == 4:
                    return super(DashboardItemFeedbackView, self).get(request, args, **kwargs)
            except:
                pass
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardItemFeedbackView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            context.update({
                "oi": self.oi,
            })
        return context
