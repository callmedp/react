import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myCoursesData = (data) => {

    const url = `my-courses/?page=${data}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

const boardNeoUser = (data) =>{
    const url = `${siteDomain}/api/v1/dashboard-neo-board-user/`
    return BaseApiService.post(url, data)
}

export default {
    myCoursesData,
    boardNeoUser
}