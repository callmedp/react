from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.core.files.uploadedfile import InMemoryUploadedFile
from partner.api.core.permissions import IsEmployeeOfVendor
from console.models import OrderItemOperations
from order.models import OrderItem

class NewOrdersVendorUpload(APIView):
    """
    List and post views for vendor to submit order associated documents.
    """
    permission_classes = (IsEmployeeOfVendor, )
    parser_classes = (MultiPartParser, )
    def get(self, request, order_item_id=None, vendor_id=None):
        uploaded_docs = OrderItemOperations.objects.filter(order_item__id=order_item_id)
        if vendor_id:
            uploaded_docs = uploaded_docs.filter(order_item__partner__id=vendor_id)
        return Response({'uploaded': True if uploaded_docs.count() else False})

    def put(self, request, order_item_id=None, vendor_id=None):
        if not vendor_id or not order_item_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            order_item = OrderItem.objects.get(id=order_item_id, partner__id=vendor_id)
        except OrderItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            import pdb; pdb.set_trace()
            order_item_operation_obj = OrderItemOperations.objects.get(order_item__id=order_item_id)
            if 'file' in request.data and isinstance(request.data['file'], InMemoryUploadedFile):
                order_item_operation_obj.uploaded_document=request.data['file']
                order_item_operation_obj.save()
                return Response(status=status.HTTP_200_OK)
        except OrderItemOperations.DoesNotExist:
            if 'file' in request.data and isinstance(request.data['file'], InMemoryUploadedFile):
                OrderItemOperations.objects.create(order_item=order_item, uploaded_document=request.data['file'])
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
