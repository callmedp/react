import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const fetchProductIds = () => {

    const url = `resume-product-id`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}?type_flow=${17}`);
};

const addToCart = (data) => {
    const url = 'cart/cart-order/';
    return BaseApiService.post(`${siteDomain}/api/v1/${url}`, data);

}


export const Api = {
    fetchProductIds, addToCart
}