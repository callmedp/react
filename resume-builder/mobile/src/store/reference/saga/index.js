import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserReference(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchUserReference, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        let data = {list: results};
        yield put({type: Actions.SAVE_USER_REFERENCE, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserReference(action) {
    try {
        let {payload: {userReference, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

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


function* bulkUpdateUserReference(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserReference, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

        console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserReference(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {referenceId} = action;

        const result = yield call(Api.deleteUserReference, candidateId, referenceId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_REFERENCE, id: referenceId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchReference() {
    yield takeLatest(Actions.FETCH_USER_REFERENCE, fetchUserReference);
    yield takeLatest(Actions.UPDATE_USER_REFERENCE, updateUserReference);
    yield takeLatest(Actions.DELETE_USER_REFERENCE, deleteUserReference);
    yield takeLatest(Actions.BULK_UPDATE_USER_REFERENCE, bulkUpdateUserReference);

}