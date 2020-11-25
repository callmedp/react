import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* populerCourses(action) {
    try {
        
        const response = yield call(Api.populerCourses);
        const result = response.data
        
        if (result["error"]) {
            return
        }
        const prds = result.data;
        const item = {'pCourseList': prds.tprds.slice(0,3)}
        yield put({ 
            type : Actions.POPULER_COURSES_FETCHED, 
            item 
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchPopulerCourses() {
    yield takeLatest(Actions.FETCH_POPULER_COURSES, populerCourses);
}