from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from order.api.core.mixins import OrderItemViewMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from order.models import Order


class OrderItemViewSet(OrderItemViewMixin, ModelViewSet):
    """
        CRUD Viewset for `OrderItem` model.
    """


# class UploadResumeShine(CreateAPIView):
#     authentication_classes = (SessionAuthentication,)
#     permission_classes = (IsAuthenticated)

#     def post(self,*args, **kwargs):
#         upload_resume_shine =self.request.POST.get('upload_resume_shine')
#         is_inbox_page =self.request.POST.get('is_inbox_page')
#         if upload_resume_shine:

#         if is_inbox_page:

#         return HttpResponse(json.dumps({'result':'updated'}), content_type="application/json")
