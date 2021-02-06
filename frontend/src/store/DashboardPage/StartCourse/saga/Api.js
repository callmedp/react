import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const getCourseURL = (data) =>{
    const url = `${siteDomain}/partner/api/v1/vendor-url/`
    return BaseApiService.post(url, data)
}

export default {
    getCourseURL
}