import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';


const fetchTrendingCnA = () => {
    const url = `trending-courses-and-skills/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
}

const fetchPopularCourses = (data) => {
    const categoryId = data?.id
    const courseOnly = data?.courseOnly
    const url = `trending-courses-and-skills/?category_id=${categoryId}&course_only=${courseOnly}`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
}


export default {
    fetchTrendingCnA,
    fetchPopularCourses
}


