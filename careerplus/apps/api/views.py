import logging

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.tasks import user_register
from order.models import Order
from shop.models import Product


class CreateOrderApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        item_list = request.data.get('item_list', [])
        name = request.data.get('name', '').strip()
        email = request.data.get('email', '').strip()
        country_code = request.data.get('country_code', '91').strip()
        mobile = request.data.get('mobile').strip()
        candidate_id = request.data.get('candidate_id', '').strip()
        if item_list:
            try:
                order = None
                flag = True
                msg = ''
                if not email and flag:
                    msg = 'email is required.'
                    flag = False
                elif not mobile and flag:
                    msg = 'mobile number is required.'
                    flag = False

                if email and not candidate_id:
                    data = {
                        "email": email,
                        "country_code": country_code,
                        "cell_phone": mobile,
                        "name": name,
                    }
                    candidate_id = user_register(data)

                if not candidate_id and flag:
                    msg = 'candidate_id is required.'
                    flag = False

                if flag:
                    order = Order.objects.create(
                        candidate_id=candidate_id,
                        email=email,
                        country_code=country_code,
                        mobile=mobile,
                        date_placed=timezone.now())

                    for data in item_list:
                        parent_id = data.get('id')
                        parent_price = data.get('price')
                        addons = data.get('addons', [])
                        variations = data.get('variations', [])
                        combos = data.get('combos', [])
                        order.orderitems.create(

                        )
                else:
                    return Response(
                        {"msg": msg, "status": 0},
                        status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                if order:
                    order.delete()
                msg = str(e)
                logging.getLogger('error_log').error(msg)
                return Response(
                    {"msg": msg, "status": 0},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"status": 0, "msg": "there is no items in order"},
                status=status.HTTP_400_BAD_REQUEST)