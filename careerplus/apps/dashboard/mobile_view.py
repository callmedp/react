from django.http import (
    HttpResponseRedirect)
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse
import logging
# from django.views.decorators.cache import never_cache
# from django.utils.decorators import method_decorator

from console.decorators import Decorate, mobile_page_only, stop_browser_cache
from order.models import OrderItem

from .dashboard_mixin import DashboardInfo


# @method_decorator(never_cache, name='dispatch')
@Decorate(stop_browser_cache())
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
            except Exception as e:
                logging.getLogger('error_log').error('unable to get dashboard item details %s' % str(e))

        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardItemDetailView, self).get_context_data(**kwargs)
        email = self.request.session.get('email')
        if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
            ops = []
            if self.oi.product.type_flow in [1, 12, 13]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163])
            elif self.oi.product.type_flow in [2, 14]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163])

            elif self.oi.product.type_flow == 3:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163])
            elif self.oi.product.type_flow == 4:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163])
            elif self.oi.product.type_flow == 5:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163])
            elif self.oi.product.type_flow == 6:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163])
            elif self.oi.product.type_flow in [7, 15]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 61, 62, 161, 162, 163])
            elif self.oi.product.type_flow == 8:
                oi_status_list = [49, 5, 46, 48, 27, 4, 161, 162, 163]
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=oi_status_list)
            elif self.oi.product.type_flow == 10:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163])
            elif self.oi.product.type_flow == 16:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 4])
            context.update({
                "oi": self.oi,
                "max_draft_limit": settings.DRAFT_MAX_LIMIT,
                "ops": list(ops),
            })
            pending_resume_items = DashboardInfo().get_pending_resume_items(
                candidate_id=self.candidate_id,
                email=email)
            context.update({
                "pending_resume_items": pending_resume_items,
            })

            if not self.request.session.get('resume_id', None):
                DashboardInfo().check_user_shine_resume(candidate_id=self.candidate_id, request=self.request)

            if self.request.session.get('resume_id', None):
                context.update({
                    "resume_id": self.request.session.get('resume_id', ''),
                    "shine_resume_name": self.request.session.get('shine_resume_name', ''),
                    "resume_extn": self.request.session.get('extension', ''),
                })
        return context


@Decorate(stop_browser_cache())
@Decorate(mobile_page_only(redirect_url='/dashboard/'))
class DashboardItemFeedbackView(TemplateView):
    template_name = 'dashboard/dashboard-itemfeedback.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi', None)
        self.rating = request.GET.get('rating')
        if self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3] and self.oi.oi_status == 4 and not self.oi.user_feedback:
                    return super(DashboardItemFeedbackView, self).get(request, args, **kwargs)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get item feedback on dashboard %s' % str(e))
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardItemFeedbackView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            context.update({
                "oi": self.oi,
                "rating":self.rating
            })
        return context


@Decorate(stop_browser_cache())
@Decorate(mobile_page_only(redirect_url='/dashboard/'))
class DashboardMobileCommentView(TemplateView):
    template_name = 'dashboard/dashboard-comment.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi')
        if self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    return super(DashboardMobileCommentView, self).get(request, args, **kwargs)
            except Exception as e:
                logging.getLogger('error_log').error('unable to view comment on mobile %s' % str(e))
                pass
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardMobileCommentView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            comments = self.oi.message_set.filter(is_internal=False).order_by('created')
            context.update({
                "oi": self.oi,
                "comments": comments
            })
        return context

    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if candidate_id:
            oi_pk = request.POST.get('oi_pk')
            comment = request.POST.get('comment', '').strip()
            try:
                oi = OrderItem.objects.get(pk=oi_pk)
                if oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3] and comment:
                    oi.message_set.create(
                        message=comment,
                        candidate_id=candidate_id,
                    )
            except Exception as e:
                logging.getLogger('error_log').error('unable to create order id message %s' % str(e))
                pass
            redirect_url = reverse("dashboard:dashboard-conversation") + '?oi=%s' % (oi.pk)
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseRedirect(reverse('dashboard:dashboard'))


@Decorate(stop_browser_cache())
@Decorate(mobile_page_only(redirect_url='/dashboard/'))
class DashboardMobileRejectView(TemplateView):
    template_name = 'dashboard/dashboard-reject.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi', None)

        if self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3] and self.oi.oi_status in [24, 46]:
                    return super(DashboardMobileRejectView, self).get(request, args, **kwargs)
            except Exception as e:
                logging.getLogger('error_log').error('unable to reject from mobile %s' % str(e))
                pass
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardMobileRejectView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            context.update({
                "obj": self.oi,
            })
        return context