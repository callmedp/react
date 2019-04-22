import {call, takeLatest, put} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";


function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchTemplate, candidateId);
        if (result['error']) {
            console.log('error');
        }
        console.log(result)

        yield put({type: Actions.SAVE_TEMPLATE, data: result['data']})
    } catch (e) {
        console.log(e);
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
}