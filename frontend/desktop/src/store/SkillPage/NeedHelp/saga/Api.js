import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'util'


const createLead = (data) => {
    const url = `tentative_url/`;
    return BaseApiService.post(`${siteDomain}/api/product/v1/${url}`, data);
};


export default {
    createLead
}