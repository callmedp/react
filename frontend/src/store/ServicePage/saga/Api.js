import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const recentAddedServices = () => {
    const url = '/api/v1/my-services';
    return BaseApiService.get(`${siteDomain}${url}`)
}


export default {
    recentAddedServices
}