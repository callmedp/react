import BaseApiService from 'services/BaseApiService'
import { siteDomain } from 'utils/domains'

const fetchProductReviews = (data) => {
    const url = `/shop/api/v1/get-prd-review/?pid=${data.prdId}&page=${data.page}`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const submitReviews = (data) => {
    const url = `/shop/api/v1/product/review/`;
    if(data?.update){
        return BaseApiService.put(`${siteDomain}${url}`, data);
    }
    return BaseApiService.post(`${siteDomain}${url}`, data);
}

const mainCourses = (id) => {
    const url = `/shop/api/v1/get-product/?pid=${id}`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const recommendedCoursesApi = (data) => {
    return BaseApiService.get(`${siteDomain}/api/v1/recommended-products/?skills=${data?.skill}&product=${data?.id}&page_size=${data?.page}`);
}

const EnquireNewSend = (data) => {
    const url = `lead-management`;
    return BaseApiService.post(`${siteDomain}/lead/api/v1/${url}/`, data);
}

const addToCartApi = (data) => {
    return BaseApiService.post(`${siteDomain}/api/v1/cart/add/`, data);
}

const addToCartRedeemApi = (data) => {
    return BaseApiService.post(`${siteDomain}/api/v1/order/direct-order/`, data);
}

const chatbotScriptApi = () => {
    let url = "";

    if(localStorage.getItem('candidateId')) url = `${siteDomain}/chatbot/api/app/learning_course_page/get-script`;
    else url = `${siteDomain}/chatbot/api/app/learning_course_non_loggedIn/get-script/`;

    return BaseApiService.get(url);
}

export default {
    mainCourses,
    fetchProductReviews,
    submitReviews,
    recommendedCoursesApi,
    EnquireNewSend,
    addToCartApi,
    addToCartRedeemApi,
    chatbotScriptApi
}   

