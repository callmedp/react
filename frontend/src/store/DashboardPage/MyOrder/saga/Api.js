import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myOrdersData = (data) => {
    const url = `my-orders/?page=${data.id}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};


export default {
    myOrdersData,
}