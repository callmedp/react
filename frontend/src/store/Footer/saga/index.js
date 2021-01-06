import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';


function* fetchTrendingCnA(action) {
    try {
        const response = yield call(Api.fetchTrendingCnA);
        if (response["error"]) {
            return
        }
        const item = response?.data?.data;
        yield put({ 
            type: Actions.TRENDING_COURSES_AND_SKILLS_FETCHED, item 
        });

    }
    catch (e) {
        console.error("Exception occured at fetchTrendingCnA Api", e);
    }
}




export default function* WatchFooter(){
    yield takeLatest(Actions.FETCH_TRENDING_COURSES_AND_SKILLS, fetchTrendingCnA);
}