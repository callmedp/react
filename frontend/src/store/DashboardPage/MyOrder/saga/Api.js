import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myOrdersData = (data) => {
    const url = `my-orders/?page=${data.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

const cancelOrder = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-cancellation/`
    return BaseApiService.post(url, data)
}

export default {
    myOrdersData,
    cancelOrder
}