import BaseApiService from "../../../services/BaseApiService";
import { shineSiteDomain, siteDomain } from '../../../utils/domains'

const trackUser = (query, userAction) => {
    let t_id = !!query['t_id'] ? query['t_id']:"";
    if(t_id == ""){
        return
    }
    let productTrackingMappingId = !!query['product_tracking_mapping_id'] ? query['product_tracking_mapping_id'].toString() : "";
    let action = userAction;
    let position = !!query['position'] ? parseInt(query['position']) : "";
    let sub_product = !!query['prod_id'] ? query['prod_id'] : "";
    let trigger_point = !!query['trigger_point']? query['trigger_point'] : "";
    let u_id = !!query['u_id']? query['u_id'] : "";
    let utm_campaign = !!query['utm_campaign']? query['utm_campaign']: "";
    let popup_based_product = !!query['popup_based_product']? query['utm_campaign'] : "";
    let domain = 2;
    let loggingData = { t_id: t_id, products: [productTrackingMappingId], action: action, 'position': position, domain: domain, 
        sub_product: sub_product, trigger_point: trigger_point, u_id: u_id, utm_campaign: utm_campaign, popup_based_product: popup_based_product }
    const url = 'learning-touchpoints-tracking/';
    return BaseApiService.post(`${shineSiteDomain}/api/v2/${url}`, loggingData, { "Content-Type": "application/json" });
}

export const Api = {
    'trackUser': trackUser,
}