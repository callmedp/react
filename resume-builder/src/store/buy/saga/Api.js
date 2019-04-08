import BaseApiService from '../../../services/BaseApiService'

const fetchProductIds = () => {

    const url = `resume-product-id`;
    return BaseApiService.get(`/api/v1/${url}?type_flow=${16}`);
};

const addToCart= (data) => {
    const url = 'cart/add-to-cart/';
    return BaseApiService.post(`/${url}`,data,{'Content-Type': 'application/x-www-form-urlencoded'}, false);

}


export const Api = {
    fetchProductIds,addToCart
}