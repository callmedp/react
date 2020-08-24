import BaseApiService from '../../../services/BaseApiService';
import { shineSiteDomain } from '../../../Utils/domains';

const trackUser = (trackingId, productTrackingMappingId, productId, action, position) => {
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: action, 'position': position, domain: 3, sub_product: productId };
    const url = 'learning-touchpoints-tracking/';
    return BaseApiService.post(`${shineSiteDomain}/api/v2/${url}`, loggingData);
}

export const Api = {
    trackUser
}