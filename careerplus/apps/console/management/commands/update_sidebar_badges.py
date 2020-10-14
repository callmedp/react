#python imports
import logging,types

#django imports
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand

#local imports

#inter app imports
from order.models import OrderItem,Order
from users.models import UserProfile,User
from partner.models import VendorHierarchy

#third party imports

def get_clean_dict(obj,data,id_based=False):
    data_to_return = {}
    for key,value in data.items():
        if not isinstance(value,types.FunctionType):
            data_to_return[key] = value
            continue

        data_to_return[key] = obj.id if id_based else obj
    return data_to_return

def invoke_user():
    logging.getLogger('info_log').info("Proxy method invoked")
    pass

key_filter_dict_mapping = {"inbox":{"order__welcome_call_done":True,
                                "order__status":1,
                                "no_process":False,
                                "oi_status__in":[5,3],
                                "product__type_flow__in":[1, 3, 12, 13]
                                },

                            "approval":{"order__welcome_call_done":True,
                                "order__status":1,
                                "no_process":False,
                                "oi_status":23,
                                "product__type_flow__in":[1, 3, 12, 13]
                                },
                            "approved":{"order__welcome_call_done":True,
                                "order__status":1,
                                "no_process":False,
                                "oi_status":24,
                                "product__type_flow__in":[1, 3, 5, 12, 13]
                                },
                            "midout":{"status":1, 
                                "orderitems__oi_status":2,
                                "orderitems__no_process":False
                                },
                            "rejected_by_admin":{"order__status":1,
                                "no_process":False,
                                "oi_status":25,
                                "product__type_flow__in":[1, 3, 12, 13],
                                "order__welcome_call_done":True
                                },

                            "rejected_by_candidate":{"order__status":1, 
                                "no_process":False,
                                "oi_status":26, 
                                "product__type_flow__in":[1, 3, 12, 13],
                                "order__welcome_call_done":True
                                },

                            "linkedin_inbox":{"order__status":1,
                                "no_process":False,
                                "product__type_flow":8,
                                "oi_status__in":[5, 3, 42],
                                "order__welcome_call_done":True
                                },

                            "linkedin_rejected_by_candidate":{"order__status":1, 
                                "oi_status":48,
                                "product__type_flow":8,
                                "order__welcome_call_done":True
                                },

                            "linkedin_rejected_by_admin":{"order__status":1, 
                                "no_process":False,
                                "oi_status":47, 
                                "product__type_flow":8,
                                "order__welcome_call_done":True
                                },

                            "linkedin_approval":{"order__status":1, 
                                "oi_status":45,
                                "product__type_flow__in":[8],
                                "order__welcome_call_done":True,
                                "assigned_to":invoke_user
                                },

                            "welcome_call_inbox":{"status":1, 
                                "welcome_call_done":False
                                },
                            
                            "welcome_call_assigned":{"assigned_to_id":invoke_user, 
                                "welcome_call_done":False,
                                "wc_cat":0
                                },

                            "welcome_call_callback":{"status":1, 
                                "welcome_call_done":False, 
                                "wc_cat":23
                                },

                            "welcome_call_issue":{"status":1, 
                                "welcome_call_done":False, 
                                "wc_cat":22
                                },
                            "domestic_profile_update":{"order__status__in":[1, 3],
                                "product__type_flow":5, 
                                "no_process":False,
                                "oi_status__in":[5, 25, 61],
                                "product__sub_type_flow__in":[501, 503],
                                "order__welcome_call_done":True
                            },

                            "domestic_profile_initiated":{"order__status__in":[1, 3],
                                "product__type_flow":5, 
                                "no_process":False,
                                "oi_status__in":[28, 4],
                                "product__sub_type_flow__in":[501, 503],
                                "order__welcome_call_done":True
                            },

                            "international_profile_update":{"order__status__in":[1, 3],
                                "product__type_flow":4, 
                                "no_process":False,
                                "oi_status__in":[5, 25, 61],
                                "order__welcome_call_done":True
                            },
                            "international_profile_approval":{"order__status":1,
                                "product__type_flow":4,
                                "oi_status":23,
                                "no_process":False,
                                "order__welcome_call_done":True
                            }
                        }

key_exclude_dict_mapping = {"inbox":{"wc_sub_cat__in":[64, 65]},
                            "approval":{"wc_sub_cat__in":[64, 65]},
                            "approved":{"wc_sub_cat__in":[64, 65]},
                            "rejected_by_admin":{"wc_sub_cat__in":[64, 65]},
                            "rejected_by_candidate":{"wc_sub_cat__in":[64, 65]},
                            "linkedin_inbox":{"wc_sub_cat__in":[64, 65]},
                            "linkedin_approval":{"wc_sub_cat__in":[64, 65],"oi_status":9},
                            "linkedin_rejected_by_candidate":{"wc_sub_cat__in":[64, 65]},
                            "linkedin_rejected_by_admin":{"wc_sub_cat__in":[64, 65]},
                            "welcome_call_inbox":{},
                            "welcome_call_assigned":{},
                            "welcome_call_callback":{},
                            "welcome_call_issue":{},
                            "midout":{},
                            "domestic_profile_update":{"wc_sub_cat__in":[64, 65]},
                            "domestic_profile_initiated":{"wc_sub_cat__in":[64, 65]},
                            "international_profile_update":{"wc_sub_cat__in":[64, 65]},
                            "international_profile_approval":{"wc_sub_cat__in":[64, 65]},
                            }

key_perm_filter_mapping = {"inbox":{
                                "order.writer_inbox_assigner":{"assigned_to__isnull":True},
                                "order.writer_inbox_assignee":{"assigned_to":invoke_user}
                            },
                            "approval":{
                                "order.can_view_all_approval_list":{},
                                "order.can_view_only_assigned_approval_list":{"assigned_to":invoke_user}
                            },
                            "approved":{
                                "order.can_view_only_assigned_approved_list":{"assigned_to":invoke_user}
                            },
                            "midout":{
                                "order.can_show_midout_queue":{}
                                },
                            "rejected_by_admin":{
                                "order.can_view_all_rejectedbyadmin_list":{},
                                "order.can_view_only_assigned_rejectedbyadmin_list":{"assigned_to":invoke_user}
                            },
                            "rejected_by_candidate":{
                                "order.can_view_all_rejectedbycandidate_list":{},
                                "order.can_view_only_assigned_rejectedbycandidate_list":{"assigned_to":invoke_user}
                            },
                            "linkedin_inbox":{
                                "order.writer_inbox_assigner":{"assigned_to":None},
                                "order.writer_inbox_assignee":{"assigned_to":invoke_user}
                            },
                            "linkedin_rejected_by_candidate":{
                                "order.can_view_all_rejectedbycandidate_list":{},
                                "order.can_view_only_assigned_rejectedbycandidate_list":{"assigned_to":invoke_user}
                            },
                            "linkedin_rejected_by_admin":{
                                "order.can_view_all_rejectedbyadmin_list":{},
                                "order.can_view_only_assigned_rejectedbyadmin_list":{"assigned_to":invoke_user}
                            },
                            "linkedin_approval":{
                                "order.can_view_all_approval_list":{},
                            },
                            "domestic_profile_update":{
                                "order.domestic_profile_update_assigner":{"assigned_to":None},
                                "order.domestic_profile_update_assignee":{"assigned_to":invoke_user}
                            },
                            "domestic_profile_initiated":{},
                            "international_profile_update":{
                                "order.international_profile_update_assigner":{"assigned_to":None},
                                "order.international_profile_update_assignee":{"assigned_to":invoke_user}
                            },
                            "international_profile_approval":{}
                        }

key_model_mapping = {'midout':Order.objects.prefetch_related('orderitems')}

def closed_filter(queue, queryset):
    q = queryset.filter(oi_status=61)
    exclude_list = []
    for oi in q:
        if queue == 'international_profile_update':
            closed_ois_count = oi.order.orderitems.filter(product__type_flow=12, \
                    oi_status=4, no_process=False).count()
            open_ois_count = oi.order.orderitems.filter(product__type_flow=12, \
                    no_process=False).count()

            if closed_ois_count != open_ois_count:
                exclude_list.append(oi.pk)
        elif queue in ['domestic_profile_update', 'domestic_profile_initiated']:
            closed_ois_count = oi.order.orderitems.filter(product__type_flow=1,\
                        product__sub_type_flow__in=[101,100], oi_status=4,\
                        no_process=False).count()
            if not closed_ois_count:
                exclude_list.append(oi.pk)

    queryset = queryset.exclude(id__in=exclude_list)

    return queryset


def cache_badges_for_writers():
    logging.getLogger('info_log').info("Started Caching Badges for Writers")

    writer_profiles = UserProfile.objects.filter(writer_type__gt=0,user__is_active=True)
    key_prefix = "writer_badges_dict_"
    oi_queues = ['inbox', 'approval', 'approved', 'midout', 'rejected_by_admin',\
            'rejected_by_candidate', 'linkedin_inbox', 'linkedin_rejected_by_candidate',\
            'linkedin_rejected_by_admin', 'linkedin_approval',\
            'domestic_profile_update', 'domestic_profile_initiated', \
            'international_profile_update', 'international_profile_approval']

    allowed_groups = ['WRITER','WRITER_HEAD']
    
    for user in User.objects.filter(is_active=True):
        
        if not user.groups.filter(name__in=allowed_groups).exists():
            continue

        data = {}
        cache_key = "{}{}".format(key_prefix,user.id)
        
        for queue in oi_queues:
            model_objects = key_model_mapping.get(queue,OrderItem.objects)
            queryset = model_objects.filter(**get_clean_dict(user,key_filter_dict_mapping[queue]))
            
            for key,value in key_exclude_dict_mapping[queue].items():
                queryset = queryset.exclude(**{key:value})

            if queue in ['international_profile_update', \
                'domestic_profile_update', 'domestic_profile_initiated']:
                queryset = closed_filter(queue, queryset)
            
            perm_dict = get_clean_dict(user,key_perm_filter_mapping[queue])
            perm_found = False

            for perm,filter_dict in key_perm_filter_mapping[queue].items():
                if user.has_perm(perm):
                    perm_found = True

                    queryset = queryset.filter(**get_clean_dict(user,filter_dict))

            data[queue] = queryset.distinct().count() if perm_found else 0

        data['allocated'] = OrderItem.objects.filter(Q(order__status__in=[1, 3], no_process=False,\
            product__type_flow__in=[1, 12, 13, 8, 3], order__welcome_call_done=True)\
            | Q(order__status__in=[1, 3], no_process=False,\
            product__sub_type_flow=101, order__welcome_call_done=False)).exclude(\
            wc_sub_cat__in=[64, 65]).exclude(oi_status=4).count()

        cache.set(cache_key,data,10*60)
        logging.getLogger('info_log').info("Cached Sidebar Badge for Writer {}".format(user.id))

    logging.getLogger('info_log').info("Finished Caching Badges for Writers")

def cache_badges_for_vendors():
    logging.getLogger('info_log').info("Started Caching Badges for Vendors")

    key_prefix = "partner_badges_dict_"
    
    for user in User.objects.filter(is_active=True):
        if not user.get_vendor_list():
            logging.getLogger('info_log').info("User {} is not associated with any vendor".format(user.id))
            continue

        data = {}
        cache_key = "{}{}".format(key_prefix,user.id)
        all_vendors = VendorHierarchy.objects.filter(employee_id=user.id,active=True).values_list('vendee',flat=True)

        data['inbox'] = OrderItem.objects.filter(Q(order__status=1, no_process=False,
            product__type_flow__in=[2, 6, 9, 10, 14, 16],order__welcome_call_done=True) & \
            (Q(product__vendor__in=all_vendors) | Q(partner__in=all_vendors) )).exclude(
            wc_sub_cat__in=[64, 65]).exclude(oi_status__in=[4, 10, 81, 161, 162, 163]).count()

        data['hold_item'] = OrderItem.objects.filter(Q(order__status=1, oi_status=10, no_process=False,
            product__type_flow__in=[2, 6, 9, 10, 14, 16],order__welcome_call_done=True) & \
            (Q(product__vendor__in=all_vendors) | Q(partner__in=all_vendors) )).exclude(
            wc_sub_cat__in=[64, 65]).count()

        data['verification_report'] = OrderItem.objects.filter(Q(order__status=1, no_process=False,
            oi_status=81, product__type_flow=6, order__welcome_call_done=True) & \
            (Q(product__vendor__in=all_vendors) | Q(partner__in=all_vendors) )).exclude(
            wc_sub_cat__in=[64, 65]).count()

        data['closed_order_item'] = OrderItem.objects.filter(Q(order__status__in= [1, 3], oi_status=4,
            no_process=False)).count()

        cache.set(cache_key,data,10*60)
        logging.getLogger('info_log').info("Cached Sidebar Badge for Vendor {}".format(user.id))

    logging.getLogger('info_log').info("Finished Caching Badges for Vendors")

def cache_badges_for_ops():
    logging.getLogger('info_log').info("Started Caching Badges for Ops")

    key_prefix = "ops_badges_dict_"

    #Initialise all Ops groups
    ops_groups = settings.WELCOMECALL_GROUP_LIST
    ops_head_groups = settings.OPS_HEAD_GROUP_LIST
    allowed_groups = ops_groups + ops_head_groups

    order_queues = ['welcome_call_inbox','welcome_call_assigned','welcome_call_issue','welcome_call_callback']

    for user in User.objects.filter(is_active=True):

        if not user.groups.filter(name__in=allowed_groups).exists():
            continue

        data = {}
        cache_key = "{}{}".format(key_prefix,user.id)

        for queue in order_queues:
            queryset = Order.objects.filter(**get_clean_dict(user,key_filter_dict_mapping[queue],id_based=True))

            for key,value in key_exclude_dict_mapping[queue].items():
                queryset = queryset.exclude(**{key:value})

            if user.groups.filter(name__in=ops_head_groups).exists():
                data[queue] = queryset.count()
                continue

            data[queue] = queryset.filter(assigned_to=user).count()

        cache.set(cache_key,data,10*60)
        logging.getLogger('info_log').info("Cached Sidebar Badge for Ops {}".format(user.id))

    logging.getLogger('info_log').info("Finished Caching Badges for Ops")


def cache_sidebar_badges():
    cache_badges_for_writers()
    cache_badges_for_vendors()
    cache_badges_for_ops()


class Command(BaseCommand):

    def handle(self,*args,**options):
        cache_sidebar_badges()


