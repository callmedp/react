import logging
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from wallet.models import Wallet ,WalletTransaction
from .serializers import WalletTransactionSerializer


class WalletTxnsHistory(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class= WalletTransactionSerializer


    def get(self,request,*args,**kwargs):
        # this is used to create the wallet if wallet doesn't exists
        candidate_id = self.request.GET.get('candidate_id',None)
        if not candidate_id:
            return super(WalletTxnsHistory, self).get(request,*args,**kwargs)
        wal_obj,created = Wallet.objects.get_or_create(owner=candidate_id)
        if created:
            logging.getLogger('info_log').info('new Wallet is created')
        return super(WalletTxnsHistory, self).get(request,*args,**kwargs)


    def get_queryset(self):

        candidate_id = self.request.GET.get('candidate_id')
        if not candidate_id:
            return WalletTransaction.objects.none()

        return WalletTransaction.objects.prefetch_related('point_txn','wallet',).filter(
            txn_type__in=[1, 2,3, 4, 5],point_value__gt=0, wallet__owner=candidate_id).order_by('-created')

        # return Wallet.objects.prefetch_related('wallettxn','point').filter(owner=candidate_id)


