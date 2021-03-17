import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {  
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    fetchReviews,
    ReviewsFetched,
    submitReview,
    fetchRecommendedCourses,
    recommendedCoursesFetched,
    sendedEnquireNow
} from './actions';

function* otherProvidersCourses(action){
    const { payload: { payload, resolve, reject} } = action;
    try{
    
        const response = yield call(Api.otherProvidersCourses);
   
        if(response?.error){
            return reject(response);
        }

        const item = response?.data;
        yield put(OtherProviderCoursesFetched({ ...item }))
        return resolve(item);
    }
    catch(e){
     
        return reject(e);
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
    
        const response = yield call(Api.fetchReviews, payload);
   
        if(response?.error){
            return reject(response);
        }

        const item = response?.data?.data;
        yield put(ReviewsFetched({ ...item }))
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
   
        if(response['error']) return resolve(response)

        return resolve(response)
    }
    catch(error){
        return resolve(error)
    }
}

function* SendEnquireNow(action) {
    const { payload: { payload, resolve, reject }} = action;

    try{
        const response = yield call(Api.EnquireNewSend, payload)

        if (response?.error) {
            return reject(response)
        }
        const item = response?.data?.data;
        return resolve(item);
    }
    catch(e) {
        console.log(`Reject sending survey question due to ${e}`);
        return reject(e);
    }
}

export default function* WatchDetailPage() {
    yield takeLatest(fetchOtherProviderCourses.type, otherProvidersCourses);
    yield takeLatest(fetchRecommendedCourses.type, recommendedCourses);
    yield takeLatest(fetchReviews.type, productReviews);
    yield takeLatest(submitReview.type, submitReviews);
    yield takeLatest(sendedEnquireNow.type, SendEnquireNow);
}
