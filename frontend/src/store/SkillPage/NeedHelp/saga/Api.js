import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const createLead = (data) => {
    const url = `lead-management/`;
    return BaseApiService.post(`${siteDomain}/lead/api/v1/${url}`, data);
};


export default {
    createLead
}