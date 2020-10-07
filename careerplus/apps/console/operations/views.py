from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.shortcuts import redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from partner.api.core.permissions import IsEmployeeOfVendor, IsAdminOrEmployeeOfVendor
from console.models import OrderItemOperations
from order.models import OrderItem

class NewOrdersVendorUpload(APIView):
    """
    List and post views for vendor to submit order associated documents.
    """
    permission_classes = (IsEmployeeOfVendor, )
    parser_classes = (MultiPartParser, )
    success_list_redirect = 'console:partner:pages:neworders-list'
    def get(self, request, orderitem_id=None, vendor_id=None):
        uploaded_docs = OrderItemOperations.objects.filter(order_item__id=orderitem_id)
        if vendor_id:
            uploaded_docs = uploaded_docs.filter(order_item__partner__id=vendor_id)
        return Response({'uploaded': None if uploaded_docs.count() == 0 else uploaded_docs[0].uploaded_document.name})

    def post(self, request, orderitem_id=None, vendor_id=None):
        if not vendor_id or not orderitem_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            vendor_id = int(vendor_id)
            orderitem_id = int(orderitem_id)
            order_item = OrderItem.objects.get(id=orderitem_id, partner__id=vendor_id)
        except OrderItem.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            order_item_operation_obj = OrderItemOperations.objects.get(order_item__id=orderitem_id)
            if 'file' in request.data and isinstance(request.data['file'], InMemoryUploadedFile):
                order_item_operation_obj.uploaded_document=request.data['file']
                order_item_operation_obj.save()
                return redirect(self.success_list_redirect, vendor_id=vendor_id)
        except OrderItemOperations.DoesNotExist:
            if 'file' in request.data and isinstance(request.data['file'], InMemoryUploadedFile):
                OrderItemOperations.objects.create(order_item=order_item, uploaded_document=request.data['file'])
                return redirect(self.success_list_redirect, vendor_id=vendor_id)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NewOrdersVendorUploadDetails(APIView):
    """
    List and post views for vendor to submit order associated documents.
    """
    permission_classes = (IsAdminOrEmployeeOfVendor, )
    def get(self, request, vendor_id=None):
        uploaded_docs = None
        if 'orderitem_ids' in request.data and isinstance(request.data['orderitem_ids'], list):
            uploaded_docs = OrderItemOperations.objects.filter(order_item__id__in=map(request.data['orderitem_ids'], int))
        if vendor_id:
            uploaded_docs = OrderItemOperations.objects.filter(order_item__partner__id=vendor_id) if not uploaded_docs \
                else uploaded_docs.filter(order_item__partner__id=vendor_id)
            response_data = {}
            for uploaded_document in uploaded_docs:
                response_data[uploaded_document.order_item.id] = uploaded_document.uploaded_document.name
            return Response(response_data)
        return Response(status=status.HTTP_404_NOT_FOUND)