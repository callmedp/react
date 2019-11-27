import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const fetchProductIds = () => {

    const url = `resume-product-id`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}?type_flow=${17}`);
};

const addToCart = (data) => {
    const url = 'cart/add-to-cart/';
    return BaseApiService.post(`${siteDomain}/${url}`, data, {'Content-Type': 'application/x-www-form-urlencoded'}, false);

}

const requestFreeResume = () => {
    const candidateId = localStorage.getItem('candidateId')
    const selectedTemplate = localStorage.getItem('selected_template',1)
    const url = `candidate/${candidateId}/free-resume/template/${selectedTemplate}/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`,{})
}

const downloadFreeResume = () => {
    const candidateId = localStorage.getItem('candidateId')
    const selectedTemplate = localStorage.getItem('selected_template',1)
    const url = `candidate/${candidateId}/free-resume/template/${selectedTemplate}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`)
}

const pollingFreeResume = () => {
    const candidateId = localStorage.getItem('candidateId')
    const url = `candidate/${candidateId}/free-resume/polling/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`)
}



export const Api = {
    fetchProductIds, addToCart,requestFreeResume,downloadFreeResume,pollingFreeResume
}