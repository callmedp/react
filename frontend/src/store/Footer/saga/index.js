import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';


function* fetchTrendingCnA(action) {
    try {
        const { payload } = action;
        const response = yield call(Api.fetchTrendingCnA, payload);
        if (response["error"]) {
            return
        }
        const item = response?.data?.data;

        if(!!payload && !!payload.homepage && !!item && item.trendingSkills instanceof Array){
            const skillList = item?.trendingSkills.reduce((rows, key, index) => 
                (index % 4 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
            
            if(skillList.length){
                item.recruiterList = skillList.slice()
            }
        }

        yield put({ 
            type: Actions.TRENDING_COURSES_AND_SKILLS_FETCHED, item 
        });

    }
    catch (e) {
        console.error("Exception occured at fetchTrendingCnA Api", e);
    }
}

function* fetchPopularCourses(action) {
    const { payload } = action
    try {
        const response = yield call(Api.fetchPopularCourses, payload);
        if (response["error"]) {
            return payload?.reject(response)
        }
        const item = response?.data?.data;
        yield put({ 
            type: Actions.POPULAR_COURSES_FETCHED, item 
        });
        return payload?.resolve(item);

    }
    catch (e) {
        console.error("Exception occured ",e)
        return payload?.reject(e);
    }
}




export default function* WatchFooter(){
    yield takeLatest(Actions.FETCH_TRENDING_COURSES_AND_SKILLS, fetchTrendingCnA);
    yield takeLatest(Actions.FETCH_POPULAR_COURSES, fetchPopularCourses);
}