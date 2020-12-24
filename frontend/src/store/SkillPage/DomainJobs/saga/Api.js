import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const domainJobs = (data) => {
    const url = `domain-jobs/?id=${data?.id}`;

    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    domainJobs,
}