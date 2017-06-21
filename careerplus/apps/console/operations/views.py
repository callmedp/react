from rest_framework.views import APIView

from console.models import OrderOperations

class NewOrdersVendorUpload(APIView):
    """
    List and post views for vendor to submit order associated documents.
    """
    def get(self, request, order_item_id):
        uploaded_docs = OrderOperations.objects.filter(order_item__id=order_item_id)
        return Response({'uploaded': True})

    def post(self, request, order_item_id):
        try:
            import pdb; pdb.set_trace()
            OrderOperations.create(request.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)