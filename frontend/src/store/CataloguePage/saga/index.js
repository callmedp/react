import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';


function* coursesAndAssessments(action) {
    const { payload } = action;

    try {

        const response = yield call(Api.coursesAndAssessments, payload);
        
        if (response["error"]) {
            return payload?.reject(response["error"])
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

        return payload?.resolve(item)

    } catch (e) {
        console.error("Exception occured ",e)
        return payload?.reject(e);
    }
}


function* recentlyAddedCourses(action){
    const { payload } = action;
    try{
        const response = yield call(Api.recentlyAddedCourses);
        console.log("recently added courses", response);
        if(!response || response['error']){
            return payload?.reject(response["error"]);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.RECENTLY_ADDED_COURSES_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        return payload?.reject(e);
    }
}




export default function* WatchCataloguePage() {
    yield takeLatest(Actions.FETCH_COURSES_AND_ASSESSMENTS, coursesAndAssessments);
    yield takeLatest(Actions.FETCH_RECENTLY_ADDED_COURSES, recentlyAddedCourses);
}