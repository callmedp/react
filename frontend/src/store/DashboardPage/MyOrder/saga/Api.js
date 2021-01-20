import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myOrdersData = (data) => {
    console.log(data)
    const url = `my-orders/?page=${data.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};


export default {
    myOrdersData,
}