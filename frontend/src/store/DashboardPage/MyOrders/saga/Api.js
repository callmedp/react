import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const orderDetails = (data) => {
    const url = `about/${data?.id}/`;
    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    orderDetails,
}