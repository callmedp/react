import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* populerCourses(action) {
    try {
        // const { payload } = action;
        // console.log("payload is ", payload)
        const response = yield call(Api.populerCourses);
        if (response["error"]) {
            return
        }
        const item = response.data;
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