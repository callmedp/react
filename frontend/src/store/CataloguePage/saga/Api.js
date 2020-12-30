import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const coursesAndAssessments = (data) => {
    const url = `courses-and-assessments/?id=${data?.id}`;

    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};

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
    coursesAndAssessments,
    recentlyAddedCourses,
    popularServices,
    trendingCategories,
    allCategories
}