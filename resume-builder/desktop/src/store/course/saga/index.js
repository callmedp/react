import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'

import {UPDATE_UI} from '../../ui/actions/actionTypes'

function* fetchUserCourse(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(Api.fetchUserCourse, candidateId);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}})

        const {data: {results}} = result;

        let data = {list: results}
        yield put({type: Actions.SAVE_USER_COURSE, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserCourse(action) {
    try {
        const {payload: {userCourse, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userCourse;
        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(id ? Api.updateUserCourse : Api.createUserCourse, userCourse, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: UPDATE_UI, data: {loader: false}})

        yield put({type: Actions.SAVE_USER_COURSE, data: result['data']});

        return resolve('User Course  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleCourseSwap(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserCourse, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

        console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserCourse(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {courseId} = action;

        const result = yield call(Api.deleteUserCourse, candidateId, courseId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_COURSE, id: courseId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchCourse() {
    yield takeLatest(Actions.FETCH_USER_COURSE, fetchUserCourse);
    yield takeLatest(Actions.UPDATE_USER_COURSE, updateUserCourse);
    yield takeLatest(Actions.DELETE_USER_COURSE, deleteUserCourse);
    yield takeLatest(Actions.HANDLE_COURSE_SWAP, handleCourseSwap);
}