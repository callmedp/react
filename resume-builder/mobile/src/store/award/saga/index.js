import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserAward(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchUserAward, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        yield put({type: Actions.SAVE_USER_AWARD, data: results[0]})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserAward(action) {
    try {
        const {payload: {userAward, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        userAward['cc_id'] = candidateId;
        const {id} = userAward;
        const result = yield call(id ? Api.updateUserAward : Api.createUserAward, userAward, candidateId, id);
        console.log('---', result);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.SAVE_USER_AWARD, data: result['data']});

        return resolve('User Award  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchAward() {
    yield takeLatest(Actions.FETCH_USER_AWARD, fetchUserAward)
    yield takeLatest(Actions.UPDATE_USER_AWARD, updateUserAward)
}