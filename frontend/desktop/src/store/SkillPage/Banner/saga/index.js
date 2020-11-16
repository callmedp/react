import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* skillPageBanner(action) {
    try {
        const { payload } = action;
        console.log("payload is ", payload)
        const response = yield call(Api.skillPageBanner, payload);
        if (response["error"]) {
            return
        }
        const item = response.data;
        console.log("breadLitem",item)
        yield put({ 
            type : Actions.SKILL_PAGE_BANNER_FETCHED, 
            item 
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchSkillPageBanner() {
    yield takeLatest(Actions.FETCH_SKILL_PAGE_BANNER, skillPageBanner);
}