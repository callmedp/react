import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const recentlyAddedCourses = () => {
    const url = '/api/v1/recent-course-added/';

    return BaseApiService.get(`${siteDomain}${url}`);
}

const popularServices = () => {
    const url = '/api/v1/popular-services/';
    
    return BaseApiService.get(`${siteDomain}${url}`);
}

const trendingCategories = () => {
    const url = '/api/v1/trending-categories/';
    
    return BaseApiService.get(`${siteDomain}${url}`);
}

const allCategories = (count) => {
    const url = `/api/v1/course-catalogue/?num=${count}`;
    
    return BaseApiService.get(`${siteDomain}${url}`);
}

export default {
    recentlyAddedCourses,
    popularServices,
    trendingCategories,
    allCategories
}   
