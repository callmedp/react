import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserReference(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchUserReference, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;

        yield put({type: Actions.SAVE_USER_REFERENCE, data: results[0]})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserReference(action) {
    try {
        let {payload: {userReference, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        userReference['cc_id'] = candidateId;
        const {id} = userReference;

        const result = yield call(id ? Api.updateUserReference : Api.createUserReference, userReference, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_REFERENCE, data: result['data']});

        return resolve('User Reference have saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchReference() {
    yield takeLatest(Actions.FETCH_USER_REFERENCE, fetchUserReference);
    yield takeLatest(Actions.UPDATE_USER_REFERENCE, updateUserReference);

}