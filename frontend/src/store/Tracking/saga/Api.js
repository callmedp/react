import BaseApiService from "../../../services/BaseApiService";
import { shineSiteDomain } from '../../../utils/domains'

const trackUser = (query, userAction) => {
    let t_id = !!query['t_id'] ? query['t_id']:"";

    if(t_id == "") {
        return;
    }

    let productTrackingMappingId = !!query['product_tracking_mapping_id'] ? query['product_tracking_mapping_id'].toString() : "";
    let action = userAction;
    let position = !!query['position'] ? parseInt(query['position']) : "";
    let sub_product = !!query['prod_id'] ? query['prod_id'] : "";
    let trigger_point = !!query['trigger_point']? query['trigger_point'] : "";
    let u_id = !!query['u_id']? query['u_id'] : "";
    let utm_campaign = !!query['utm_campaign']? query['utm_campaign']: "";
    let popup_based_product = !!query['popup_based_product']? query['utm_campaign'] : "";
    let recommendation_by = !!query['recommendation_by']? query['recommendation_by'] : "";
    // let cart_addition = !!query['cart_addition']? query['cart_addition'] : "";
    let domain = 2;
    let loggingData = { t_id: t_id, products: [productTrackingMappingId], action: action, 'position': position, domain: domain, 
        sub_product: sub_product, trigger_point: trigger_point, u_id: u_id, utm_campaign: utm_campaign, popup_based_product: popup_based_product, recommendation_by: recommendation_by }
    
    const url = 'learning-touchpoints-tracking/';
    
    // if(cart_addition === 'True'){
    //     let cartLoggingData = { t_id: t_id, products: [productTrackingMappingId], action: 'direct_cart_addition', 'position': position, domain: domain, 
    //     sub_product: sub_product, trigger_point: trigger_point, u_id: u_id, utm_campaign: utm_campaign, popup_based_product: popup_based_product, recommendation_by: recommendation_by }
    //     BaseApiService.post(`${shineSiteDomain}/api/v2/${url}`, cartLoggingData, { "Content-Type": "application/json" });
    // }
    // else if(cart_addition === 'False'){
    //     let cartLoggingData = { t_id: t_id, products: [productTrackingMappingId], action: 'cart_addition_product_page', 'position': position, domain: domain, 
    //     sub_product: sub_product, trigger_point: trigger_point, u_id: u_id, utm_campaign: utm_campaign, popup_based_product: popup_based_product, recommendation_by: recommendation_by }
    //     BaseApiService.post(`${shineSiteDomain}/api/v2/${url}`, cartLoggingData, { "Content-Type": "application/json" });
    // } 

    return BaseApiService.post(`${shineSiteDomain}/api/v2/${url}`, loggingData, { "Content-Type": "application/json" });
}

export const Api = {
    'trackUser': trackUser,
}