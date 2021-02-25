import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'
import { CountryCode2 } from 'utils/storage';

const recentlyAddedCourses = (payload) => {
    const code2 = payload?.code2 || CountryCode2() || 'IN';
    const url = `/api/v1/recent-course-added/?code2=${code2}`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const popularServices = (payload) => {
    const code2 = payload?.code2 || CountryCode2() || 'IN';
    const url = `/api/v1/popular-services/?code2=${code2}`;

    return BaseApiService.get(`${siteDomain}${url}`);
}

const trendingCategories = (payload) => {
    const code2 = payload?.code2 || CountryCode2() || 'IN';
    const url = `/api/v1/trending-categories/?code2=${code2}`;

    return BaseApiService.get(`${siteDomain}${url}`);
}

const allCategories = (payload) => {
    const url = `/api/v1/course-catalogue/?num=${payload?.num}`;

    return BaseApiService.get(`${siteDomain}${url}`);
}

export default {
    recentlyAddedCourses,
    popularServices,
    trendingCategories,
    allCategories
}   
