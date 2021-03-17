import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {  
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    mainCoursesFetched,
    fetchMainCourses,
    CourseReviewFetched,
    fetchCourseReview
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

function* courseReviewsApi(action){
    const { payload: {values}, resolve, reject } = action;
    try {
        const response = yield call(Api.courseReviews, values);

        if(response?.error) return reject(response);

        console.log(response);
        const item = response?.data?.data?.prd_reviews;
        yield put(CourseReviewFetched({ ...item }));
        return resolve(item);
    }
    catch(e) {
        return e;
    }
}

export default function* WatchDetailPage() {
    yield takeLatest(fetchOtherProviderCourses.type, otherProvidersCourses);
    yield takeLatest(fetchMainCourses.type, mainCoursesApi);
    yield takeLatest(fetchCourseReview.type, courseReviewsApi);
}
