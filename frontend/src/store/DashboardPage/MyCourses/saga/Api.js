import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myCoursesData = (data) => {
    let url = "";
    url = `my-courses/?page=${data?.page}&last_month_from=${data?.last_month_from}&select_type=${data?.select_type}`;
    
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