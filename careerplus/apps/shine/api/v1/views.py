from rest_framework.generics import CreateAPIView
from django.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse,HttpResponseBadRequest
from core.api_mixin import ShineCandidateDetail
from order.models import OrderItem,Order
from django.conf import settings
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from wsgiref.util import FileWrapper
import json,logging




class UploadResumeShine(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self,*args, **kwargs):
        import ipdb; ipdb.set_trace()
        upload_after_service = self.request.POST.get('upload_after_service','')

        if upload_after_service:
            order_id = self.request.POST.get('order_id','')
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
            return HttpResponseBadRequest(json.dumps({'result':'Order item id not provided'}), content_type="application/json")

        order_item = OrderItem.objects.filter(id=order_item_id).first()

        if not order_item:
            return HttpResponseBadRequest(json.dumps({'result':'Order item id not exist'}), content_type="application/json")

        
        
        candidate_id = order_item.order.candidate_id
        file = None
        try:
            file_path = settings.RESUME_DIR + order_item.oi_resume.name
            if not settings.IS_GCP:
                file = open(file_path,'rb')
            else:
                file = GCPPrivateMediaStorage().open(file_path)
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
        
        data={
            'candidate_id':candidate_id,
            'upload_medium':'direct',
            'upload_source':'web',
            # 'resume_source':7,
            # 'resume_medium':7,
            # 'resume_trigger':7
        }

        files={
            'resume_file':file
        }

        response = ShineCandidateDetail().upload_resume_shine(data=data,files=files)
        if not settings.IS_GCP:
            file.close()
        if response:
            order_item.service_resume_upload_shine = True
            order_item.save()
            return HttpResponse(json.dumps({'result':'uploaded to shine'}), content_type="application/json")
        return HttpResponseBadRequest()
