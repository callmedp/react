import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* coursesAndAssessments(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {

        const response = yield call(Api.coursesAndAssessments, payload);

        if (response["error"]) {
            return reject(response)
        }
        const item = response.data;
    
        var courseList = item.courses
        var assessmentList = item.assessments
        if(!!payload && !payload.medium){
            //converts 1D array to 2D array
            courseList = !!item && item.courses?.length ? item.courses.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];
        
            //converts 1D array to 2D array
            assessmentList = !!item && item.assessments?.length ? item?.assessments.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];
        }
        
        yield put({ 
            type : Actions.COURSES_AND_ASSESSMENTS_FETCHED, 
            item : { courseList , assessmentList }
        })

        return resolve(item)

    } catch (e) {
        return reject(e);
    }
}




export default function* WatchCoursesAndAssessments() {
    yield takeLatest(Actions.FETCH_COURSES_AND_ASSESSMENTS, coursesAndAssessments);
}