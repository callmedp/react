import {Api} from './Api';
import {apiError} from '../../../Utils/apiError';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getUIStatus = state => state.ui;

function* fetchUserExperience(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const ui = yield select(getUIStatus)
        if(!ui.mainloader){
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }

        if (localStorage.getItem('experience')) {

            let local_data = JSON.parse(localStorage.getItem('experience')) && JSON.parse(localStorage.getItem('experience')).length ? 
                            JSON.parse(localStorage.getItem('experience')) :
                            [{
                                "candidate_id": '',
                                "id": '',
                                "job_profile": '',
                                "company_name": '',
                                "start_date": '',
                                "end_date": '',
                                "is_working": false,
                                "job_location": '',
                                "work_description": '',
                                "order": 0
                            }]

            yield put({type: Actions.SAVE_USER_EXPERIENCE, data: {list:local_data}})
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserExperience, candidateId);
        if (result['error']) {
            apiError();
        }
        let {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        results.map((el) => {
            let job_profile = el.job_profile
            el.job_profile = {label:job_profile,value:job_profile}
        })
        let data = {list: results}
        if(! data.list.length){
            data = {
                ...data,
                ...{
                    list: [
                            {
                                "candidate_id": '',
                                "id": '',
                                "job_profile": '',
                                "company_name": '',
                                "start_date": '',
                                "end_date": '',
                                "is_working": false,
                                "job_location": '',
                                "work_description": '',
                                "order": 0
                            }
                        ]
                }
            };
        }

        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: data})
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        apiError();
    }
}


function* bulkUserExperienceUpdate(action) {
    try {
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        let {payload: {list,resolve,reject}} = action;
        list.map((el) => {
            let label =  el.job_profile && el.job_profile.label
            el.job_profile = label
         })
        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserExperience, list, candidateId);

        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('experience')){
                localStorage.removeItem('experience')
                yield call(fetchUserExperience)
            }
            yield put({type: Actions.SAVE_USER_EXPERIENCE, data: {list: result['data']}})
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');

        }

    } catch (e) {
        apiError();
    }
}


function* deleteUserExperience(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const {experienceId} = action;

        const result = yield call(Api.deleteUserExperience, candidateId, experienceId);


        if (result['error']) {
            apiError();
        }
        yield put({type: Actions.REMOVE_EXPERIENCE, id: experienceId});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        yield call(fetchUserExperience)
        

    } catch (e) {
        apiError();
    }
}


function* fetchJobTitlesAndSuggestions(action) {
    try {

        const {payload: {inputValue, suggestionType, resolve, reject}} = action;
        const apiResult = yield call(Api.fetchJobTitlesAndSuggestions, inputValue, suggestionType);


        if (apiResult['error']) {
            apiError();
            return reject(new SubmissionError({_error: apiResult['errorMessage']}));
        }

        let {data: {result}} = apiResult;

        if (!suggestionType) {
            result = (result || []).map((el) => ({
                label: el, value: el.toString()
            }))
            return resolve(result);
        }

        yield  put({type:uiAction.SAVE_SUGGESTIONS, data: {suggestions: result}});
        resolve([])
    } catch (e) {
        apiError();
    }
}

export default function* watchExperience() {
    yield takeLatest(Actions.FETCH_USER_EXPERIENCE, fetchUserExperience);
    yield takeLatest(Actions.DELETE_USER_EXPERIENCE, deleteUserExperience);
    yield takeLatest(Actions.BULK_UPDATE_USER_EXPERIENCE, bulkUserExperienceUpdate);
    yield takeLatest(Actions.FETCH_EXPERIENCE_LIST, fetchJobTitlesAndSuggestions);
}