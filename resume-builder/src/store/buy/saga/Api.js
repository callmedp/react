import BaseApiService from '../../../services/BaseApiService'

const fetchProductIds = () => {

    const url = `resume-product-id`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/${url}/`);
};


export const Api = {
    fetchProductIds
}