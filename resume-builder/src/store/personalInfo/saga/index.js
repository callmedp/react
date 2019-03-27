import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* getPersonalDetails(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchPersonalInfo, candidateId);
        if (result['error']) {
            console.log('error');
        }
        // localStorage.setItem('candidateId', result.data && result.data['candidate_id'] || '');

    } catch (e) {
        console.log(e);
    }
}

function* updatePersonalDetails(action) {
    try {
        const {payload: {personalDetails, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.updatePersonalData, personalDetails, candidateId);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.SAVE_USER_INFO, data: result['data']});

        return resolve('User Personal  Info saved successfully.');

    } catch (e) {

        console.log('error', e);
    }
}

export default function* watchPersonalInfo() {
    yield takeLatest(Actions.FETCH_PERSONAL_INFO, getPersonalDetails)
    yield takeLatest(Actions.UPDATE_PERSONAL_INFO, updatePersonalDetails)
}