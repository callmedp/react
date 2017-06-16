from rest_framework.views import APIView

from console.operations.models import Snippet
from console.operations.SnippetSerializer

class NewOrdersVendorUpload(APIView):
    """
    List and post views for vendor to submit order associated documents.
    """
    def get(self, request, order_item_id):
        uploaded_docs = OrderOperations.objects.filter(order_item__id=order_item_id)
        return Response({'uploaded': True})

    def post(self, request, order_item_id):
        try:
            OrderOperations.create(request.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)