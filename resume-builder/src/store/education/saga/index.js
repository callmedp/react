import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'

import {courseTypeList} from "../../../Utils/courseTypeList";


function* fetchUserEducation(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchUserEducation, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        let data = results[0];
        data = {
            ...results[0],
            ...{
                course_type: courseTypeList[data['course_type']]
            }
        }
        yield put({type: Actions.SAVE_USER_EDUCATION, data: data})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserEducation(action) {
    try {
        const {payload: {userEducation, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        userEducation['cc_id'] = candidateId;
        const {id} = userEducation;
        console.log('--user Education-');
        const result = yield call(id ? Api.updateUserEducation : Api.createUserEducation, userEducation, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }


        yield put({type: Actions.SAVE_USER_EDUCATION, data: result['data']});

        return resolve('User Education  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchEducation() {
    yield takeLatest(Actions.FETCH_USER_EDUCATION, fetchUserEducation)
    yield takeLatest(Actions.UPDATE_USER_EDUCATION, updateUserEducation)
}