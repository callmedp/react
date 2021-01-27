import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

// fetch reviews
const myReviewsData = (data) => {
    const url = `review/?product_id=${data.prod}&page=${data.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

const saveReviewsData = (data) => {
    const url = `review/`;
    return BaseApiService.post(`${siteDomain}/dashboard/api/v1/${url}`, data);
};

export default {
    myReviewsData,
    saveReviewsData,
}