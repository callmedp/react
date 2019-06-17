import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import {initialState} from '../reducer';


function* fetchUserProject(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        if (localStorage.getItem('project')) {
            let data = {list: JSON.parse(localStorage.getItem('project')) || []}
            yield put({
                type: Actions.SAVE_USER_PROJECT,
                data: data.list.length ? data : initialState
            });
            return;
        }

        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.fetchUserProject, candidateId);
        if (result['error']) {
            console.log('error');
        }

        yield put({type: UPDATE_UI, data: {loader: false}});

        let {data: {results}} = result;
        if (!results.length) {
            const state = yield select();
            let {project: {list}} = state;
            results = list
        }
        let data = results.length ? {list: results} : initialState


        yield put({type: Actions.SAVE_USER_PROJECT, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserProject(action) {
    try {
        let {payload: {userProject, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userProject;

        yield put({type: UPDATE_UI, data: {loader: true}})


        const result = yield call(id ? Api.updateUserProject : Api.createUserProject, userProject, candidateId, id);


        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('project');

        yield put({type: UPDATE_UI, data: {loader: false}})

        yield put({type: Actions.SAVE_USER_PROJECT, data: result['data']});

        return resolve('User Project have saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleProjectSwap(action) {
    try {


        let {payload: {list, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.bulkUpdateUserProject, list, candidateId);

        yield put({type: UPDATE_UI, data: {loader: false}});

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('project');

        let {data} = result;

        data.sort((a, b) => a.order <= b.order);

        data = {list: data}


        yield put({type: Actions.SAVE_USER_PROJECT, data: data})


        return resolve('User Education  Info saved successfully.');


    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserProject(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {projectId} = action;

        const result = yield call(Api.deleteUserProject, candidateId, projectId);


        if (result['error']) {
            console.log(result['error'])
        }
        localStorage.removeItem('project');

        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_PROJECT, id: projectId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchProject() {
    yield takeLatest(Actions.FETCH_USER_PROJECT, fetchUserProject);
    yield takeLatest(Actions.UPDATE_USER_PROJECT, updateUserProject);
    yield takeLatest(Actions.DELETE_USER_PROJECT, deleteUserProject);
    yield takeLatest(Actions.HANDLE_PROJECT_SWAP, handleProjectSwap);
    yield takeLatest(Actions.BULK_U_C_USER_PROJECT, handleProjectSwap);

}