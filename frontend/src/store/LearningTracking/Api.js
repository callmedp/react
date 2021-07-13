import BaseApiService from 'services/BaseApiService'
import { trackingSiteDomain } from 'utils/domains'

const learningTrackingApi = (data) => {
    console.log("final tracking data", data)
    return BaseApiService.post(`${trackingSiteDomain}/demo-tracking-api/`, data);
}

export default {
    learningTrackingApi
}   

