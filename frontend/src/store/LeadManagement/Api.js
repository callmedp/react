import BaseApiService from 'services/BaseApiService'
import { siteDomain } from 'utils/domains'

const leadManagementApi = (data) => {
    return BaseApiService.post(`${siteDomain}/lead/api/v1/lead-management/`, data);
}

export default {
    leadManagementApi,
}   

