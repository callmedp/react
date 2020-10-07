from django.views.generic.base import TemplateView, View
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

class ScoreCheckerView(TemplateView):
    # template_name = 'resumescorechecker/index.html'
    def get(self,request,**kwargs):
        return HttpResponsePermanentRedirect("{}{}".format(settings.RESUME_SHINE_MAIN_DOMAIN, request.get_full_path()))


class ScoreCheckerView2(TemplateView):
    template_name = 'resumescorechecker/inner.html'


class ScoreCheckerViewMobile(TemplateView):
    template_name = 'resumescorechecker/index.html'