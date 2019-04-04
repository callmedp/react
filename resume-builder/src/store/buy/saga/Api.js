import BaseApiService from '../../../services/BaseApiService'

const fetchProductIds = () => {

    const url = `resume-product-id`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/${url}?type_flow=${16}`);
};

const addToCart= (data) => {
    console.log('data<><><><>',data)
    const url = 'cart/add-to-cart/';
    return BaseApiService.post(`http://127.0.0.1:8000/${url}`,data,{'Content-Type': 'application/x-www-form-urlencoded'}, false);

}


export const Api = {
    fetchProductIds,addToCart
}