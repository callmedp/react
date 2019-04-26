import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const fetchProductIds = () => {

    const url = `resume-product-id`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}?type_flow=${16}`);
};

const addToCart= (data) => {
    const url = 'cart/add-to-cart/';
    return BaseApiService.post(`${siteDomain}/${url}`,data,{'Content-Type': 'application/x-www-form-urlencoded'}, false);

}


export const Api = {
    fetchProductIds,addToCart
}