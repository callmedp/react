import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserSkill(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchUserSkill, candidateId);
        if (result['error']) {
            console.log('error');
        }
        console.log('--get user experiences Info---', result);
        yield put({type: Actions.SAVE_USER_SKILL, data: result['data']})
    } catch (e) {
        console.log(e);
    }
}

//
// function* updatePersonalDetails(action) {
//     try {
//         const {payload: {personalDetails, resolve, reject}} = action;
//
//         const candidateId = localStorage.getItem('candidateId') || '';
//
//         const result = yield call(Api.updatePersonalData, personalDetails, candidateId);
//         if (result['error']) {
//             return reject(new SubmissionError({_error: result['errorMessage']}));
//         }
//         yield put({type: Actions.SAVE_USER_INFO, data: result['data']});
//
//         return resolve('User Personal  Info saved successfully.');
//
//     } catch (e) {
//
//         console.log('error', e);
//     }
// }

export default function* watchSkill() {
    yield takeLatest(Actions.FETCH_USER_SKILL, fetchUserSkill)
}