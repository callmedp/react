import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'
import {proficiencyList} from "../../../Utils/proficiencyList";


function* fetchUserSkill(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchUserSkill, candidateId);
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
        yield put({type: Actions.SAVE_USER_SKILL, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserSkill(action) {
    try {
        let {payload: {userSkill, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        userSkill['cc_id'] = candidateId;
        const {id} = userSkill;

        const result = yield call(id ? Api.updateUserSkill : Api.createUserSkill, userSkill, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_SKILL, data: result['data']});

        return resolve('User Skill  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchSkill() {
    yield takeLatest(Actions.FETCH_USER_SKILL, fetchUserSkill);
    yield takeLatest(Actions.UPDATE_USER_SKILL, updateUserSkill);
}