import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'

import {UPDATE_UI, SAVE_SUGGESTIONS} from '../../ui/actions/actionTypes'
import {initialState} from '../reducer/index'


function* fetchUserExperience(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';


        if (localStorage.getItem('experience')) {
            let data = {list: JSON.parse(localStorage.getItem('experience')) || []}
            yield put({
                type: Actions.SAVE_USER_EXPERIENCE,
                data: data.list.length ? data : initialState
            });

            return;
        }
        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.fetchUserExperience, candidateId);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}});

        let {data: {results}} = result;

        if (!results.length) {
            const state = yield select();
            let {experience: {list}} = state;
            results = list
        }
        let data = results.length ? {list: results} : initialState

        data = {
            ...data,
            ...{
                list: (data.list || []).map(el => {
                    el['job_profile'] = {
                        value: el['job_profile'],
                        label: el['job_profile']
                    }
                    return el;
                })
            }
        }
        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: data})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserExperience(action) {
    try {
        let {payload: {userExperience, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userExperience;

        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(id ? Api.updateUserExperience : Api.createUserExperience, userExperience, candidateId, userExperience.id);

        yield put({type: UPDATE_UI, data: {loader: false}})

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('experience');


        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: result['data']});

        return resolve('User Experience  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleExperienceSwap(action) {
    try {
        let {payload: {list, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.bulkUpdateUserExperience, list, candidateId);

        yield put({type: UPDATE_UI, data: {loader: false}});


        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('experience');

        let {data} = result;

        data.sort((a, b) => a.order <= b.order);


        data = {list: data};

        console.log('--data in the ---', data);

        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: data})

        return resolve('User Experience  Info saved successfully.');


    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserExperience(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {experienceId} = action;

        const result = yield call(Api.deleteUserExperience, candidateId, experienceId);


        if (result['error']) {
            console.log(result['error'])
        }
        localStorage.removeItem('experience');

        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EXPERIENCE, id: experienceId});

    } catch (e) {
        console.log('error', e);
    }
}

function* fetchJobTitlesAndSuggestions(action) {
    try {

        const {payload: {inputValue, suggestionType, res, rej}} = action;
        const apiResult = yield call(Api.fetchJobTitlesAndSuggestions, inputValue, suggestionType);


        if (apiResult['error']) {
            return rej(new SubmissionError({_error: apiResult['errorMessage']}));
        }

        let {data: {result}} = apiResult;

        if (!suggestionType) {
            result = (result || []).map((el) => ({
                label: el, value: el.toString()
            }))
            return res(result);
        }

        yield  put({type: SAVE_SUGGESTIONS, data: {suggestions: result}});
        res([])
    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchExperience() {
    yield takeLatest(Actions.FETCH_USER_EXPERIENCE, fetchUserExperience);
    yield takeLatest(Actions.UPDATE_USER_EXPERIENCE, updateUserExperience);
    yield takeLatest(Actions.DELETE_USER_EXPERIENCE, deleteUserExperience);
    yield takeLatest(Actions.HANDLE_EXPERIENCE_SWAP, handleExperienceSwap);
    yield takeLatest(Actions.BULK_U_C_USER_EXPERIENCE, handleExperienceSwap);
    yield takeLatest(Actions.FETCH_EXPERIENCE_LIST, fetchJobTitlesAndSuggestions);
}