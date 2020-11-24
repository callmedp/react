import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const populerCourses = () => {
    const url = `trending-courses/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
};

export default {
    populerCourses,
}