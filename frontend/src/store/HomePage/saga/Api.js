import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const latestBlog = () => {
    const url = '/api/v1/latest-blogs/';

    return BaseApiService.get(`${siteDomain}${url}`);
}

const mostViewedCourse = () => {
    const url = '/api/v1/most-viewed-courses/';

    return BaseApiService.get(`${siteDomain}${url}`);
}

const inDemandProducts = () => {
    const url = '/api/v1/in-demand-product/';

    return BaseApiService.get(`${siteDomain}${url}`);
}

const jobAssistanceServices = () => {
    const url = '/api/v1/job-assistance-services/';

    return BaseApiService.get(`${siteDomain}${url}`);
}

export default {
    latestBlog,
    mostViewedCourse,
    inDemandProducts,
    jobAssistanceServices,
}   

