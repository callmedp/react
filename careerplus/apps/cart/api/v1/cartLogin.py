from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
import logging


class PaymentLoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_classes = None

    def post(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        cart_obj=None
        candidate_id = request.data.get('candidate_id')
        cart_pk = request.data.get('cart_pk')
        email = request.data.get('email')
        name = request.data.get('name')
        country_code = request.data.get('country_code','+91')
        mobile = request.data.get('mobile')
        first_name,last_name =None,None

        if name:
            first_name = name.strip().split(' ')[0]
            last_name = ' '.join((name + ' ').split(' ')[1 :]).strip()

        if not candidate_id or not cart_pk:
            return Response({'error':'Unable to update the cart '},status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_obj = Cart.objects.get(id=cart_pk)
        except:
            logging.getLogger('error_log').error('unable to get cart')
            return Response({'error':'Cart Not Found'},status=status.HTTP_400_BAD_REQUEST)

        if first_name:
            cart_obj.first_name = first_name
        if last_name:
            cart_obj.last_name = last_name
        if mobile:
            cart_obj.mobile = mobile
        if email:
            cart_obj.owner_email = email
            cart_obj.email = email
        cart_obj.country_code = country_code

        cart_obj.save()

        return Response({'redirect':'/cart/payment-option/'},status=status.HTTP_200_OK)
        

