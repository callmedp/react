import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {  
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    mainCoursesFetched,
    fetchMainCourses,
    fetchReviews,
    ReviewsFetched,
    submitReview,
} from './actions';

function* mainCoursesApi(action){
    const { payload, resolve, reject } = action;

    try {
        const response = yield call(Api.mainCourses, payload.id);

        if(response?.error) return reject(response);
        const item = response?.data?.data;
        yield put(mainCoursesFetched({ ...item }));
        return resolve(item);
    }
    catch(e) {
        return e;
    }
}

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
    
        const response = yield call(Api.submitReview, payload);
   
        if(response?.error){
            return reject(response);
        }

        const item = response?.data?.data;
        return resolve(item);
    }
    catch(e){
     
        return reject(e);
    }
}

export default function* WatchDetailPage() {
    yield takeLatest(fetchOtherProviderCourses.type, otherProvidersCourses);
    yield takeLatest(fetchMainCourses.type, mainCoursesApi);
    yield takeLatest(fetchReviews.type, productReviews);
    yield takeLatest(submitReview.type, submitReviews);
}
