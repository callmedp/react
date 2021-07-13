import BaseApiService from 'services/BaseApiService'
import { siteDomain } from 'utils/domains'

const learningTrackingApi = (data) => {
    console.log("final tracking data", data)
    return BaseApiService.post(`${siteDomain}/demo-tracking-api/`, data);
}

export default {
    learningTrackingApi
}   

