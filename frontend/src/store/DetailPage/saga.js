import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {  
    mainCoursesFetched,
    fetchMainCourses,
    fetchProductReviews,
    ReviewsFetched,
    submitReview,
    fetchRecommendedCourses,
    recommendedCoursesFetched,
    sendEnquireNow,
    fetchAddToCartEnroll,
    fetchAddToCartRedeem
} from './actions';
import {siteDomain} from '../../utils/domains';

function* mainCoursesApi(action){
    const { payload: { payload, resolve, reject } } = action;

    try {
        const response = yield call(Api.mainCourses, payload.id);
        if(response?.error) return reject(response);
        const item = response?.data?.data;

        if(item?.redirect_url) return reject(item);

        if(!!payload && payload.device === 'desktop' && !!item && !!item.product_detail && item.product_detail.pop_list instanceof Array) {
            const otherProvidersList = item.product_detail.pop_list.reduce((rows, key, index) => 
                (index % 4 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
            if(otherProvidersList.length){
                item.product_detail.pop_list = otherProvidersList.slice();
            }
        }
        
        yield put(mainCoursesFetched({ ...item }));
        return resolve(item);
    }
    catch(e) {
        return e;
    }
}

function* recommendedCourses(action){
    const { payload: { payload, resolve, reject} } = action;
    try{
    
        const response = yield call(Api.recommendedCoursesApi, payload);
   
        if(response?.error){
            return reject(response);
        }

        const item = response?.data;

        if(!!payload && payload.device === 'desktop' && !!item && item.results instanceof Array) {
            const courseLikeList = item.results.reduce((rows, key, index) => 
                (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
            if(courseLikeList.length){
                item.results = courseLikeList.slice();
            }
        }

        yield put(recommendedCoursesFetched({ ...item }))
        return resolve(item);
    }
    catch(e){
     
        return reject(e);
    }
}

function* productReviews(action){
    const { payload: { payload, resolve, reject} } = action;
    try{
    
        const response = yield call(Api.fetchProductReviews, payload);
   
        if(response?.error){
            return reject(response);
        }

        const item = response?.data?.data;

        if(!!payload && payload.device === 'desktop' && !!item && item.prd_reviews.prd_review_list instanceof Array) {
            const reviewsList = item?.prd_reviews?.prd_review_list.reduce((rows, key, index) => 
                (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
            
            if(reviewsList.length) item.prd_reviews.prd_review_list = reviewsList.slice();
        }

        if(!!payload && payload.device) yield put(ReviewsFetched({ ...item, device: payload.device }));
        return resolve(item);
    }
    catch(e){
     
        return reject(e);
    }
}

function* submitReviews(action){
    const { payload: { payload, resolve, reject} } = action;
    try{
    
        const response = yield call(Api.submitReviews, payload);
        if(response['error']) return resolve(response);

        return resolve(response);
    }
    catch(error){
        return resolve(error)
    }
}

function* SendEnquireNow(action) {
    const { payload: { payload, resolve, reject }} = action;

    try {
        const response = yield call(Api.EnquireNewSend, payload)

        if (response?.error) return reject(response);

        const item = response?.data?.data;
        return resolve(item);
    }
    catch(e) {
        console.log(`Reject sending survey question due to ${e}`);
        return reject(e);
    }
}

function* AddToCart(action) {
    const { payload: { cartItems, resolve, reject }} = action;

    try {
        const response = yield call(Api.addToCartApi, cartItems)

        if (response?.error) return reject(response);

        const item = response?.data?.data;
        if(cartItems.cart_type === 'cart') return window.location.href = `${siteDomain}${item.cart_url}`;
        else if(cartItems.cart_type === 'express') return window.location.href = `${siteDomain}${item.redirect_url}`;
    }
    catch(e) {
        console.log(`Reject sending survey question due to ${e}`);
        return reject(e);
    }
}

function* AddToCartRedeem(action) {
    const { payload: { cartItems, resolve, reject }} = action;

    try {
        const response = yield call(Api.addToCartRedeemApi, cartItems)

        if (response?.error) return reject(response);

        const item = response?.data?.data;
        if(item.status === 1) return window.location.href = `${siteDomain}${item.redirectUrl}`;
        else resolve(item);
    }
    catch(e) {
        console.log(`Reject sending survey question due to ${e}`);
        return reject(e);
    }
}

export default function* WatchDetailPage() {
    yield takeLatest(fetchMainCourses.type, mainCoursesApi);
    yield takeLatest(fetchRecommendedCourses.type, recommendedCourses);
    yield takeLatest(fetchProductReviews.type, productReviews);
    yield takeLatest(submitReview.type, submitReviews);
    yield takeLatest(sendEnquireNow.type, SendEnquireNow);
    yield takeLatest(fetchAddToCartEnroll.type, AddToCart);
    yield takeLatest(fetchAddToCartRedeem.type, AddToCartRedeem);
}
