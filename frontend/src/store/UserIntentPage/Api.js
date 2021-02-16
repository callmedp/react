import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const userIntentData = (data) => {
    const url = `/api/v1/user-intent/?${data.data.type}`
    
    return BaseApiService.post(`${siteDomain}${url}`, data);
}

export default {
    userIntentData
}