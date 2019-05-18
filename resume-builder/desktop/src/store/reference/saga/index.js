import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import { initialState } from '../reducer';


function* fetchUserReference(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        if (localStorage.getItem('reference')) {
            let data = {list: JSON.parse(localStorage.getItem('reference')) || []}
            yield put({
                type: Actions.SAVE_USER_REFERENCE,
                data: data.list.length ? data : initialState
            });
            return;
        }

        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(Api.fetchUserReference, candidateId);
        if (result['error']) {
            console.log('error');
        }

        yield put({type: UPDATE_UI, data: {loader: false}})

        let {data: {results}} = result;

        if (!results.length) {
            const state = yield select();
            let {reference: {list}} = state;
            results = list
        }

        let data = results.length ? {list: results} : initialState
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

        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(id ? Api.updateUserReference : Api.createUserReference, userReference, candidateId, id);

        yield put({type: UPDATE_UI, data: {loader: false}})

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('reference');

        yield put({type: Actions.SAVE_USER_REFERENCE, data: result['data']});

        return resolve('User Reference have saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleReferenceSwap(action) {
    try {
        let {payload: {list, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserReference, list, candidateId);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('reference');

        let {data} = result;

        data.sort((a, b) => a.order <= b.order);

        data = {list: data};


        yield put({type: Actions.SAVE_USER_REFERENCE, data: data});

        return resolve('User Reference  Info saved successfully.');


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

        localStorage.removeItem('reference');

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
    yield takeLatest(Actions.HANDLE_REFERENCE_SWAP, handleReferenceSwap);
    yield takeLatest(Actions.BULK_U_C_USER_REFERENCE, handleReferenceSwap);


}