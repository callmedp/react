import requests
import logging
import json

from django.conf import settings
from django.views.generic import (DetailView,ListView,View)
from django.shortcuts import redirect,reverse,render

from .utils import VskillTest
from shop.models import Category


class VskillTestView(DetailView):
    template_name = 'vskill/vskill_test.html'

    def get(self,request, *args, **kwargs):
        test_id = self.request.GET.get('test_id','')

        vskill_object = VskillTest()

        token = vskill_object.get_token()
        if not token:
            return redirect(reverse('homepage'))

        # all_test = self.get_all_test(token)
        # if not all_test:
        #     redirect(reverse('homepage'))

        single_test = vskill_object.get_test_by_id(token,test_id)
        if not single_test:
            return redirect(reverse('homepage'))
        return render(request,self.template_name,{'single_test': single_test})


class AssessmentLandingPage(View):
    template_name = 'vskill/vskill_landing.html'

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)














