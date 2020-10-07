import logging
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wallet.models import Wallet ,WalletTransaction
from .serializers import WalletTransactionSerializer


class WalletTxnsHistory(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class= None

    def get(self, request, *args, **kwargs) :
        # this is used to create the wallet if wallet doesn't exists
        candidate_id = self.request.GET.get('candidate_id', None)
        if not candidate_id :
            return super(WalletTxnsHistory, self).get(request, *args, **kwargs)
        wal_obj, created = Wallet.objects.get_or_create(owner=candidate_id)
        if created :
            logging.getLogger('info_log').info('new Wallet is created')
            return Response('wallet created',status=status.HTTP_201_CREATED)
        wal_txns = wal_obj.wallettxn.prefetch_related('point_txn','order','usedpoint','usedpoint__point').filter(
            txn_type__in=[1, 2, 3,
                                                                                                             4, 5],
                                                                 point_value__gt=0).order_by(
            '-created')
        new_data = [{"created":txn.created.strftime("%b %d, %Y"),
                     "get_txn_type":txn.get_txn_type(),
                     "order":txn.order.number if txn.order else'',
                     "txn": txn.txn,
                     "status":txn.status,
                     "notes":txn.notes,
                     "point_value":txn.point_value,
                     "added_point_expiry":txn.added_point_expiry().strftime("%b %d, "
                                                                                    "%Y")if txn.added_point_expiry()
                     else '',
                     "current_value":txn.current_value } for txn in wal_txns]

        return Response({"wal_total":wal_obj.get_current_amount(),"txns":new_data},status=status.HTTP_200_OK)



# class WalletTxnsHistory(ListAPIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serializer_class= WalletTransactionSerializer
#
#
#     def get(self,request,*args,**kwargs):
#         # this is used to create the wallet if wallet doesn't exists
#         candidate_id = self.request.GET.get('candidate_id',None)
#         if not candidate_id:
#             return super(WalletTxnsHistory, self).get(request,*args,**kwargs)
#         wal_obj,created = Wallet.objects.get_or_create(owner=candidate_id)
#         if created:
#             logging.getLogger('info_log').info('new Wallet is created')
#         return super(WalletTxnsHistory, self).get(request,*args,**kwargs)
#
#
#     def get_queryset(self):
#
#         candidate_id = self.request.GET.get('candidate_id')
#         if not candidate_id:
#             return WalletTransaction.objects.none()
#
#         return WalletTransaction.objects.prefetch_related('point_txn','wallet',).filter(
#             txn_type__in=[1, 2,3, 4, 5],point_value__gt=0, wallet__owner=candidate_id).order_by('-created')
#
#         # return Wallet.objects.prefetch_related('wallettxn','point').filter(owner=candidate_id)
#
#
