import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* coursesAndAssessments(action) {
    try {
        const { payload } = action;
        const response = yield call(Api.coursesAndAssessments, payload);
        console.log("response is ", response)
        if (response["error"]) {
            return
        }
        const item = response.data;
        yield put({ 
            type : Actions.COURSES_AND_ASSESSMENTS_FETCHED, 
            item
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchCoursesAndAssessments() {
    yield takeLatest(Actions.FETCH_COURSES_AND_ASSESSMENTS, coursesAndAssessments);
}