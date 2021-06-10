import BaseApiService from 'services/BaseApiService'
import { siteDomain } from 'utils/domains'

const learningTrackingtApi = (data) => {
    return BaseApiService.post(`${siteDomain}/demo-tracking-api/`, data);
}

export default {
    learningTrackingtApi
}   

