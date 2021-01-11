import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';


const fetchTrendingCnA = () => {
    const url = `trending-courses-and-skills/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
}

const fetchPopularCourses = (data) => {
    const categoryId = data
    const url = `trending-courses-and-skills/?category_id=${categoryId}`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
}


export default {
    fetchTrendingCnA,
    fetchPopularCourses
}


