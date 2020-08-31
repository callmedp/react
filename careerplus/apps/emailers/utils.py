import bson
import logging
import datetime

from shop.models import ShineProfileData
from django.db.models import Q
from pymongo import MongoClient
from django.conf import settings
from core.api_mixin import FeatureProfileUpdate


class BadgingMixin(object):
    CANDIDATE_MONGO_PORT = settings.CANDIDATE_MONGO_PORT
    CANDIDATE_MONGO_USERNAME = settings.CANDIDATE_MONGO_USERNAME
    CANDIDATE_MONGO_PASSWORD = settings.CANDIDATE_MONGO_PASSWORD
    CANDIDATE_MONGO_INSTANCE_STR = settings.CANDIDATE_MONGO_INSTANCE_STR
    CANDIDATE_MONGO_DB = settings.CANDIDATE_MONGO_DB

    def __init__(self):
        connection_string = 'mongodb://{}:{}@{}/{}'.format(
            self.CANDIDATE_MONGO_USERNAME, self.CANDIDATE_MONGO_PASSWORD,
            self.CANDIDATE_MONGO_INSTANCE_STR, self.CANDIDATE_MONGO_DB
        )
        conn = MongoClient(connection_string)
        database = conn[self.CANDIDATE_MONGO_DB]
        self.coll = database['CandidateStatic']

    def get_existing_badge_value(self, candidate_id):
        # this is to determine that this candidate id mongo db bson id.
        if bson.objectid.ObjectId.is_valid(candidate_id):
            candidate_id = bson.ObjectId(candidate_id)

        candidate = self.coll.find_one({"_id": candidate_id}, {"scp": 1})

        if candidate:
            if candidate.get('scp'):
                return candidate.get('scp')
            else:
                return {}

    def get_badging_value_for_order(self, candidate_id, curr_order_item):
        if curr_order_item.product.sub_type_flow in [1602, 201]:
            filter_kwargs = {
                'vendor': curr_order_item.product.vendor,
                'sub_type_flow': curr_order_item.product.sub_type_flow
            }
        else:
            filter_kwargs = {
                'sub_type_flow': curr_order_item.product.sub_type_flow
            }
        current_sub_type_flow = ShineProfileData.objects.filter(
            **filter_kwargs)
        if current_sub_type_flow.first():
            return current_sub_type_flow.first().id

    def sort_as_per_priority(self, existing_badge_value):
        ec_values = existing_badge_value.get('ec', [])
        if ec_values:
            sorted_ec_values = list(ShineProfileData.objects.filter(
                id__in=ec_values
            ).order_by('-priority_value').values_list('id', flat=True))
            existing_badge_value['ec'] = sorted_ec_values
        return existing_badge_value

    def get_badging_data(self, candidate_id, curr_order_item=None, feature=False, touch_point=False):
        existing_badge_value = self.get_existing_badge_value(candidate_id)
        if existing_badge_value is None:
            return None
        if candidate_id and curr_order_item:
            new_value = self.get_badging_value_for_order(
                candidate_id, curr_order_item)
            if feature:
                existing_values = existing_badge_value.get('ec', [])
                existing_values.append(new_value)
                final_values = list(set(existing_values))
                existing_badge_value['ec'] = final_values
            elif touch_point:
                existing_values = existing_badge_value.get('tp', [])
                touch_data = {'pid': curr_order_item.product.id, 'name': curr_order_item.product.name,
                              'start': curr_order_item.added_on}
                if curr_order_item.product.type_flow == 1:
                    touch_data.update(
                        {'end': curr_order_item.added_on + datetime.timedelta(days=30)})
                else:
                    touch_data.update({'end': curr_order_item.end_date})
                existing_values.append(touch_data)
                existing_badge_value['tp'] = existing_values
            else:
                try:
                    existing_badge_value.get('ec', []).remove(new_value)
                except ValueError:
                    logging.getLogger('error_log').error(
                        'unfeature values does not exist in ec')
                    return None

        existing_badge_value = self.sort_as_per_priority(existing_badge_value)
        return existing_badge_value

    def get_specificKey(self, product):
        if product.type_flow in [1, 3, 13, 17, 18, 19]:
            return 'las'
        elif product.type_flow in [2, 4]:
            return 'lac'
        elif product.type_flow in [16]:
            return 'laa'
        elif product.sub_type_flow in [502]:
            return 'las'
        else:
            return 'las'

    def get_active_services_or_courses_or_assessments(self, candidate_id, curr_order_item=None, active=False):
        active_values = self.get_existing_badge_value(candidate_id)
        if active_values is None:
            return None
        if candidate_id and curr_order_item:
            key = self.get_specificKey(curr_order_item.product)

            if active:
                existing_values = active_values.get(key, [])
                existing_values.append(curr_order_item.product.id)
                active_values[key] = list(set(existing_values))
            else:
                try:
                    active_values.get(key, []).remove(
                        curr_order_item.product.id)
                except Exception as e:
                    logging.getLogger('error_log').error(
                        ' Product Id {} is not available in key {}'.format(curr_order_item.product.id, key))

        return active_values

    def update_badging_data(self, candidate_id, data):
        data = {
            'ShineCareerPlus': data
        }
        flag = FeatureProfileUpdate().update_feature_profile(
            candidate_id=candidate_id, data=data
        )

        return flag
