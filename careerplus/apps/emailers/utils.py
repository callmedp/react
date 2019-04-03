
from shop.models import ShineProfileData
from order.models import OrderItem


def get_featured_profile_data_for_candidate(candidate_id, curr_order_item, feature):

    feature_profile_items_sub_type_flow = list(ShineProfileData.objects.all().values_list('sub_type_flow',flat=True))
    current_sub_type_flow = ShineProfileData.objects.filter(sub_type_flow=curr_order_item.product.sub_type_flow)
    if feature:
        data = {"ShineCareerPlus": {'ec': [current_sub_type_flow.first().id]}}
        current_ecs_value = list(current_sub_type_flow.values('id', 'priority_value'))
    else:
        data = {"ShineCareerPlus": {'ec': []}}
        current_ecs_value = []

    other_featured_items = OrderItem.objects.filter(
        order__candidate_id=candidate_id,
        product__type_flow=5,
        product__sub_type_flow__in=feature_profile_items_sub_type_flow,
        oi_status=28
    ).exclude(id=curr_order_item.id)

    if other_featured_items.exists():
        other_active_sub_type_flow = list(set(other_featured_items.values_list('product__sub_type_flow', flat=True)))
        other_feature_profile_items = list(ShineProfileData.objects.filter(
            sub_type_flow__in=other_active_sub_type_flow
        ).order_by('-priority_value', '-id').values('id', 'priority_value'))
        current_ecs_value.extend(other_feature_profile_items)
        current_ecs_value = list(sorted(current_ecs_value, key=lambda x: x['id'], reverse=True))
        current_ecs_value = list(sorted(current_ecs_value, key=lambda x: x['priority_value'], reverse=True))
        final_values = []
        for val in current_ecs_value:
            if val['id'] not in final_values:
                final_values.append(val['id'])

        data['ShineCareerPlus']['ec'] = final_values
    # get feature profile flow id
    feature_profile_item_id = ShineProfileData.objects.filter(sub_type_flow=501).first().id
    if feature:
        if feature_profile_item_id in data['ShineCareerPlus']['ec']:
            data['ShineCareerPlus']['xfr'] = 1
    else:
        if curr_order_item.product.sub_type_flow == 501 and feature_profile_item_id not in data['ShineCareerPlus']['ec'] :
            data['ShineCareerPlus']['xfr'] = 0
        elif feature_profile_item_id in data['ShineCareerPlus']['ec']:
            data['ShineCareerPlus']['xfr'] = 1

    return data
