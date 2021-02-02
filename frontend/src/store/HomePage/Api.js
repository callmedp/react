import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const mostViewedCourse = (data) => {
    const url = `/api/v1/most-viewed-courses/?category_id=${data.categoryId}`;

    return BaseApiService.get(`${siteDomain}${url}`);
}

const inDemandProducts = (data) => {
    const url = `/api/v1/in-demand-product/?page_id=${data.pageId}&tab_type=${data.tabType}`;

    return BaseApiService.get(`${siteDomain}${url}`);
}

const jobAssistanceAndBlogs = () => {
    const url = '/api/v1/job-assistance-latest-blogs/';

    return BaseApiService.get(`${siteDomain}${url}`);
}

export default {
    mostViewedCourse,
    inDemandProducts,
    jobAssistanceAndBlogs,
}   

