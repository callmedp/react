import BaseApiService from '../../../services/BaseApiService';
import { shineSiteDomain } from '../../../Utils/domains';

const trackUser = (trackingId, productTrackingMappingId, productId,
         action, position, triggerPoint, uId, utmCampaign) => {
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: action,
             'position': position, domain: 2, sub_product: productId, trigger_point : triggerPoint,
            u_id : uId, utm_campaign : utmCampaign };
    const url = 'learning-touchpoints-tracking/';
    return BaseApiService.post(`${shineSiteDomain}/api/v2/${url}`, loggingData);
}

export const Api = {
    trackUser
}