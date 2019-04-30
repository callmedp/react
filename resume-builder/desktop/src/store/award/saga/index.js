import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import {UPDATE_UI} from '../../ui/actions/actionTypes'

import {SubmissionError} from 'redux-form'
import {proficiencyList} from "../../../Utils/proficiencyList";


function* fetchUserAward(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        if (localStorage.getItem('award')) {

            yield put({type: Actions.SAVE_USER_AWARD, data: JSON.parse(localStorage.getItem('award')) || []})
            return;
        }

        yield put({type: UPDATE_UI, data: {loader: true}})
        const result = yield call(Api.fetchUserAward, candidateId);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}})

        const {data: {results}} = result;
        let data = {list: results};
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
        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(id ? Api.updateUserAward : Api.createUserAward, userAward, candidateId, id);

        yield put({type: UPDATE_UI, data: {loader: false}})

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }


        //delete the award
        localStorage.removeItem('award');
        yield put({type: Actions.SAVE_USER_AWARD, data: result['data']});

        return resolve('User Award  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleAwardSwap(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserAward, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

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
    yield takeLatest(Actions.HANDLE_AWARD_SWAP, handleAwardSwap);
}