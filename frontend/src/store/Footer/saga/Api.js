import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';


const fetchTrendingCnA = (data) => {
    let query='';
    if(!!data.homepage){
        query='homepage=True'
    }
    const url = `trending-courses-and-skills/?${query}&num_courses=${data.numCourses}`;
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


