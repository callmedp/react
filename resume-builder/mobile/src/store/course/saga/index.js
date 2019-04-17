import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserCourse(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchUserCourse, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;

        yield put({type: Actions.SAVE_USER_COURSE, data: results[0]})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserCourse(action) {
    try {
        const {payload: {userCourse, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        userCourse['cc_id'] = candidateId;
        const {id} = userCourse;

        const result = yield call(id ? Api.updateUserCourse : Api.createUserCourse, userCourse, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_COURSE, data: result['data']});

        return resolve('User Course  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchCourse() {
    yield takeLatest(Actions.FETCH_USER_COURSE, fetchUserCourse)
    yield takeLatest(Actions.UPDATE_USER_COURSE, updateUserCourse)
}