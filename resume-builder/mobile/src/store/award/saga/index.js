import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'
import {proficiencyList} from "../../../Utils/proficiencyList";


function* fetchUserAward(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchUserAward, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        console.log("Sorted list ")
        console.log(results)
        let data = {list: results};
        console.log('---', data);
        yield put({type: Actions.SAVE_USER_AWARD, data: data})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserAward(action) {
    try {
        const {payload: {userAward, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

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


function* bulkUpdateUserAward(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserAward, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

        console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserAward(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {awardId} = action;

        const result = yield call(Api.deleteUserAward, candidateId, awardId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_AWARD, id: awardId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchAward() {
    yield takeLatest(Actions.FETCH_USER_AWARD, fetchUserAward);
    yield takeLatest(Actions.UPDATE_USER_AWARD, updateUserAward);
    yield takeLatest(Actions.DELETE_USER_AWARD, deleteUserAward);
    yield takeLatest(Actions.BULK_UPDTATE_USER_AWARD, bulkUpdateUserAward);
}