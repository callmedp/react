from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView,View
from django.core.cache import  cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from payment.tasks import make_logging_request
from .mixins import SessionManagerMixin


class WriteResumeView(TemplateView):
    template_name = 'resumebuilder/index.html'

    def get(self, request, *args, **kwargs):
        tracking_id = request.GET.get('t_id', '')
        utm_campaign = request.GET.get('utm_campaign', '')
        trigger_point = request.GET.get('trigger_point', '')
        u_id = request.GET.get('u_id', request.session.get('u_id',''))
        position = request.GET.get('position', -1)
        product_tracking_mapping_id = 11

        if tracking_id:
            request.session.update({
                'tracking_id': tracking_id,
                'trigger_point': trigger_point,
                'position': position,
                'u_id': u_id,
                'utm_campaign': utm_campaign,
                'product_tracking_mapping_id': product_tracking_mapping_id})

        tracking_id= request.session.get('tracking_id','')
        tracking_product_id= request.session.get('tracking_product_id','')
        position= request.session.get('position',position)
        u_id= request.session.get('u_id',u_id)
        utm_campaign= request.session.get('utm_campaign',utm_campaign)

        if tracking_id and product_tracking_mapping_id:
            make_logging_request.delay(
                        tracking_product_id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id, utm_campaign, 2)

        return render(request, self.template_name)

class FreeResumeDownload(View):
    template_name = "admin/free-resume-downloads.html"

    def get(self, request, *args, **kwargs):
        has_permission = request.user.is_superuser
        free_resume_downloads = cache.get('free_resume_downloads')
        if not has_permission:
            raise PermissionDenied()
        return render(request, self.template_name, {'free_resume_downloads':
                                        free_resume_downloads})

    def post(self,request,*args,**kwargs):
        cache.set('free_resume_downloads',request.POST.get('free_downloads',0),timeout=None)
        free_resume_downloads = cache.get('free_resume_downloads')
        return render(request, self.template_name, {'free_resume_downloads':
                                        free_resume_downloads,'success':True})
