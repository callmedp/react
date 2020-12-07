import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';



function* navOffersAndTags(action) {
    try {
        const { payload } = action;
        const response = yield call(Api.navOffersAndTags, payload);
        if (response["error"]) {
            return
        }
        const item = response?.data?.data;

        yield put({ 
            type : Actions.NAVIGATION_OFFERS_AND_SPECIAL_TAGS_FETCHED, 
            item 
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchNavOffersAndTags() {
    yield takeLatest(Actions.FETCH_NAVIGATION_OFFERS_AND_SPECIAL_TAGS, navOffersAndTags);
}