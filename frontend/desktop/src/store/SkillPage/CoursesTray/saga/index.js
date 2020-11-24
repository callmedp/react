import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* coursesAndAssessments(action) {
    try {
        const { payload } = action;
        const response = yield call(Api.coursesAndAssessments, payload);
        
        if (response["error"]) {
            return
        }
        const item = response.data;

        //converts 1D array to 2D array
        const courseList = !!item && item.courses?.length ? item.courses.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];
        
        //converts 1D array to 2D array
        const assessmentList = !!item && item.assessments?.length ? item?.assessments.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];
        

        yield put({ 
            type : Actions.COURSES_AND_ASSESSMENTS_FETCHED, 
            item : { courseList , assessmentList }
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchCoursesAndAssessments() {
    yield takeLatest(Actions.FETCH_COURSES_AND_ASSESSMENTS, coursesAndAssessments);
}