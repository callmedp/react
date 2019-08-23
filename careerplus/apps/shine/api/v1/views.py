from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse,HttpResponseBadRequest
from core.api_mixin import ShineCandidateDetail 
from order.models import OrderItem,Order
from django.conf import settings
import json,logging




class UploadResumeShine(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self,*args, **kwargs):
        upload_after_service = self.request.POST.get('upload_after_service','')

        if upload_after_service:
            order_id = self.request.POST.get('order_id','-1')
            order = Order.objects.filter(id =order_id).first()
            if not  order:
                return HttpResponseBadRequest(json.dumps({'result':'No Order'}), content_type="application/json")
            order_items = order.orderitems.all()
            for oi in order_items:
                oi.service_resume_upload_shine = True if oi.product.type_flow == 1 else False
                oi.save()
            return HttpResponse(json.dumps({'result':'Resume will be updated to shine'}), content_type="application/json")
            

        order_item_id = int(self.request.POST.get('order_item_id',''))

        if not order_item_id:
            return HttpResponseBadRequest(json.dumps({'result':'Order item id does not provided'}), content_type="application/json")

        order_item = OrderItem.objects.filter(id=order_item_id).first()

        if not order_item:
            return HttpResponseBadRequest(json.dumps({'result':'Order item does not exist'}), content_type="application/json")

        
        
        candidate_id = order_item.order.candidate_id
        data={
            'candidate_id':candidate_id,
            'upload_medium':'direct',
            'upload_source':'web',
            # 'resume_source':7,
            # 'resume_medium':7,
            # 'resume_trigger':7
        }
        file_path = settings.RESUME_DIR + order_item.oi_resume.name
        response = ShineCandidateDetail().upload_resume_shine(data=data,file_path=file_path)
        if response:
            order_item.service_resume_upload_shine = True
            order_item.save()
            return HttpResponse(json.dumps({'result':'uploaded to shine'}), content_type="application/json")
        return HttpResponseBadRequest()
