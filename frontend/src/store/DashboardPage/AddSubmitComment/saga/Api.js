import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const getOiComment = (data) => {
    const url = `${siteDomain}/api/v1/order-item-comment/?oi_pk=${data.oi_id}`
    return BaseApiService.get(url)
}

const postOiComment = (data) => {
    const url = `${siteDomain}/api/v1/order-item-comment/`
    return BaseApiService.post(url, data)
}

export default {
    getOiComment,
    postOiComment,
}