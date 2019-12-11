from django.shortcuts import render

# Create your views here.

from django.views.generic.base import TemplateView,View
from django.core.cache import  cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


from .mixins import SessionManagerMixin


class WriteResumeView(TemplateView):
    template_name = 'resumebuilder/index.html'

class FreeResumeDownload(View):
    template_name = "admin/free-resume-downloads.html"

    def get(self, request, *args, **kwargs):
        has_permission = request.user.is_superuser
        free_resume_downloads = cache.get('free_resume_downloads', 1)
        if not has_permission:
            raise PermissionDenied()
        return render(request, self.template_name, {'free_resume_downloads':
                                        free_resume_downloads})

    def post(self,request,*args,**kwargs):
        cache.set('free_resume_downloads',request.POST.get('free_downloads',1))
        free_resume_downloads = cache.get('free_resume_downloads', 1)
        return render(request, self.template_name, {'free_resume_downloads':
                                        free_resume_downloads,'success':True})
