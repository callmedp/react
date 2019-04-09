import logging
from django.core.management.base import BaseCommand
from emailers.utils import get_featured_profile_data_for_candidate
from core.api_mixin import FeatureProfileUpdate
from order.models import OrderItem

from shop.mixins import CourseCatalogueMixin


class Command(BaseCommand, CourseCatalogueMixin):
    """
    Custom command to Update xfr value to ec value on shine site for feature profile data.
    """
    help = 'Update xfr value to ec value on shine site for feature profile data'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        featured_orderitems = OrderItem.objects.filter(
            order__status__in=[1, 3], product__type_flow=5, oi_status=28, product__sub_type_flow__in=[501])
        count = 0
        logging.getLogger('info_log').info("Started:- No. of order items changed from xfr to ec are %s" % str(featured_orderitems.count()))
        for obj in featured_orderitems:
            candidate_id = obj.order.candidate_id

            if candidate_id:
                try:
                    data = get_featured_profile_data_for_candidate(
                        candidate_id=candidate_id, curr_order_item=obj, feature=True)
                    flag = FeatureProfileUpdate().update_feature_profile(
                        candidate_id=candidate_id, data=data)
                    if flag:
                        count += 1
                        logging.getLogger('info_log').info(
                            "Data- %s || Candidate Id- %s || OrderItemId - %s" % (str(data),str(candidate_id), str(obj.id))
                        )
                except Exception as e:
                    print(str(e))
                    logging.getLogger('error_log').error(
                        "Error Occured for order item %s while changing from xfr to ec- %s " % (str(obj.id), str(e)))

        logging.getLogger('info_log').info("End- No. of order items changed from xfr to ec are %s" % str(count))
