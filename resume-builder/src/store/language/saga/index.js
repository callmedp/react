import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import {proficiencyList} from "../../../Utils/proficiencyList";
import {SubmissionError} from 'redux-form'


function* fetchUserLanguage(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchUserLanguage, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        let data = results[0];
        data = {
            ...data,
            ...{
                proficiency: proficiencyList[data['proficiency'].toString()]
            }
        }
        yield put({type: Actions.SAVE_USER_LANGUAGE, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserLanguage(action) {
    try {
        let {payload: {userLanguage, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        userLanguage['cc_id'] = candidateId;
        const {id} = userLanguage;

        const result = yield call(id ? Api.updateUserLanguage : Api.createUserLanguage, userLanguage, candidateId, id);
        console.log('---lang ',result);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_LANGUAGE, data: result['data']});

        return resolve('User Language  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchLanguage() {
    yield takeLatest(Actions.FETCH_USER_LANGUAGE, fetchUserLanguage);
    yield takeLatest(Actions.UPDATE_USER_LANGUAGE, updateUserLanguage)
}