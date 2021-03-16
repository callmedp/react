import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {  
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    mainCoursesFetched,
    fetchMainCourses
} from './actions';

function* mainCoursesApi(action){
    const { payload, resolve, reject } = action;
    console.log(payload);
    try {
        const response = yield call(Api.mainCourses, payload.id);
        console.log(response);
        if(response?.error){
            return reject(response);
        }
        const item = response;
        yield put(mainCoursesFetched({ ...item }))
        return resolve(item);
    }
    catch(e){
     
        return reject(e);
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

export default function* WatchDetailPage() {
    yield takeLatest(fetchOtherProviderCourses.type, otherProvidersCourses);
    yield takeLatest(fetchMainCourses.type, mainCoursesApi);
}
