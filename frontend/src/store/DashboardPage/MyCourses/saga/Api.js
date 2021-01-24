import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myCoursesData = (data) => {
    const url = `my-courses/?page=${data}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};


export default {
    myCoursesData,
}