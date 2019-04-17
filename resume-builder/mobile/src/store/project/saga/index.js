import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserProject(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchUserProject, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;

        yield put({type: Actions.SAVE_USER_PROJECT, data: results[0]})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserProject(action) {
    try {
        let {payload: {userProject, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        userProject['cc_id'] = candidateId;
        const {id} = userProject;

        const result = yield call(id ? Api.updateUserProject : Api.createUserProject, userProject, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_PROJECT, data: result['data']});

        return resolve('User Project have saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchProject() {
    yield takeLatest(Actions.FETCH_USER_PROJECT, fetchUserProject)
    yield takeLatest(Actions.UPDATE_USER_PROJECT, updateUserProject)
}