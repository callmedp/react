import {call, takeLatest, put} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import {UPDATE_UI} from "../../ui/actions/actionTypes";


function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const result = yield call(Api.fetchTemplate, candidateId,action.payload.template);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}});

        yield put({type: Actions.SAVE_TEMPLATE, data: result['data']})
    } catch (e) {
        console.log(e);
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
}