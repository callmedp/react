import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const domainJobs = (payload) => {
    const url = `domain-jobs/?id=${payload?.id}`;
    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    domainJobs,
}