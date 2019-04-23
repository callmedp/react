import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'



function* fetchUserEducation(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchUserEducation, candidateId);
        if (result['error']) {
            console.log('error');
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        let data = {list: results};
        data = {
            ...data,
            ...{
                list: data['list']
            }
        };

        yield put({type: Actions.SAVE_USER_EDUCATION, data: data})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserEducation(action) {
    try {
        const {payload: {userEducation, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userEducation;
        console.log('--user Education-');
        const result = yield call(id ? Api.updateUserEducation : Api.createUserEducation, userEducation, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        return resolve('User Education  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* bulkUpdateUserEducation(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserEducation, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

        console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserEducation(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {educationId} = action;

        const result = yield call(Api.deleteUserEducation, candidateId, educationId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EDUCATION, id: educationId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchEducation() {
    yield takeLatest(Actions.FETCH_USER_EDUCATION, fetchUserEducation);
    yield takeLatest(Actions.UPDATE_USER_EDUCATION, updateUserEducation);
    yield takeLatest(Actions.DELETE_USER_EDUCATION, deleteUserEducation);
    yield takeLatest(Actions.BULK_UPDATE_USER_EDUCATION , bulkUpdateUserEducation);

}