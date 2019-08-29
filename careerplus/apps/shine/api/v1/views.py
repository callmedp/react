#django addons
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse,HttpResponseBadRequest
from django.conf import settings

#in apps import 
from core.api_mixin import ShineCandidateDetail 
from order.models import OrderItem,Order
from order.tasks import upload_Resume_shine
from shared.rest_addons.authentication import ShineUserAuthentication

#python imports
import json,logging

class UploadResumeShine(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,*args, **kwargs):
        upload_after_service = self.request.POST.get('upload_after_service','')

        if upload_after_service:
            order_id = self.request.POST.get('order_id','-1')
            order = Order.objects.filter(id =order_id).first()
            if not  order:
                return HttpResponseBadRequest(json.dumps({'result':'No Order'}), content_type="application/json")
            order.service_resume_upload_shine = json.loads(self.request.POST.get('upload_flag_value','true'))
            order.save()
            if order.service_resume_upload_shine:
                return HttpResponse(json.dumps({'result':'Resume will be updated to shine','upload_to_shine':True}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'result':'Resume will not be updated to shine','upload_to_shine':False}), content_type="application/json")
            

        order_item_id = int(self.request.POST.get('order_item_id',''))
        upload_Resume_shine.delay(order_item_id)

        return HttpResponse(json.dumps({'result':'Resume will be uploaded to shine'}), content_type="application/json")
