import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const getRecommendedData = (data) => {
    const url = `recommended-courses-and-assesments/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
};


export default {
    getRecommendedData
}
