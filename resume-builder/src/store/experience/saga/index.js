import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserExperience(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchUserExperience, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: results[0]})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserExperience(action) {
    try {
        let {payload: {userExperience, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        userExperience['cc_id'] = candidateId;
        const {id} = userExperience;

        const result = yield call(id ? Api.updateUserExperience : Api.createUserExperience, userExperience, candidateId, userExperience.id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: result['data']});

        return resolve('User Experience  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchExperience() {
    yield takeLatest(Actions.FETCH_USER_EXPERIENCE, fetchUserExperience)
    yield takeLatest(Actions.UPDATE_USER_EXPERIENCE, updateUserExperience)
}