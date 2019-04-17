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
        let data = {list: results};
        data = {
            ...data,
            ...{
                list: data['list'].map(el => {
                    return {
                        ...el,
                        proficiency: proficiencyList[el['proficiency'].toString()]
                    }
                })
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


function* bulkSaveUserSkill(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkSaveUserSkill, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

        console.log('---', result);

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserSkill(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {skillId} = action;

        const result = yield call(Api.deleteUserSkill, candidateId, skillId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserSkill)
        yield put({type: Actions.REMOVE_SKILL, id: skillId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchSkill() {
    yield takeLatest(Actions.FETCH_USER_SKILL, fetchUserSkill);
    yield takeLatest(Actions.UPDATE_USER_SKILL, updateUserSkill);
    yield takeLatest(Actions.DELETE_USER_SKILL, deleteUserSkill);
    yield takeLatest(Actions.BULK_SAVE_USER_SKILL, bulkSaveUserSkill);
}