import BaseApiService from 'services/BaseApiService'
import { trackingSiteDomain } from 'utils/domains'

const learningTrackingApi = (data) => {
    console.log("final tracking data", data)
    return BaseApiService.post(`${trackingSiteDomain}/api/v1/core/track`, data);
}

export default {
    learningTrackingApi
}   




