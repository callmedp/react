import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';


const fetchTrendingCnA = () => {
    const url = `trending-courses-and-skills/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
}




export default {
    fetchTrendingCnA,
}


