import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

function* getPersonalDetails(action) {
    try {
        const result = yield call(Api.fetchPersonalInfo);
        console.log('result is -----', result);
        if (result['error']) {
            console.log('error');
        }
    } catch (e) {
        console.log(e);
    }


}

export default function* watchPersonalInfo() {
    yield takeLatest(Actions.FETCH_PERSONAL_INFO, getPersonalDetails)
}