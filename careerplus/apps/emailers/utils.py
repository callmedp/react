
from shop.models import ShineProfileData
from order.models import OrderItem


def get_featured_profile_data_for_candidate(candidate_id, curr_order_item, feature):
    feature_profile_items_sub_type_flow = list(ShineProfileData.objects.all().values_list('sub_type_flow',flat=True))
    current_sub_type_flow = ShineProfileData.objects.filter(sub_type_flow=curr_order_item.product.sub_type_flow)
    if feature:
        data = {"ShineCareerPlus": {'ec': [current_sub_type_flow.first().id]}}
    else:
        data = {"ShineCareerPlus": {'ec': []}}
    other_featured_items = OrderItem.objects.filter(
        order__candidate_id=candidate_id,
        product__type_flow=5,
        product__sub_type_flow__in=feature_profile_items_sub_type_flow,
        oi_status=28
    ).exclude(id=curr_order_item.id)
    if other_featured_items.exists():
        other_active_sub_type_flow = list(set(other_featured_items.values_list('product__sub_type_flow', flat=True)))
        other_feature_profile_items = list(ShineProfileData.objects.filter(sub_type_flow__in=other_active_sub_type_flow).values_list('id', flat=True))
        data['ShineCareerPlus']['ec'].extend(other_feature_profile_items)
    final_data = list(set(data['ShineCareerPlus']['ec']))
    data['ShineCareerPlus']['ec'] = final_data
    return data
