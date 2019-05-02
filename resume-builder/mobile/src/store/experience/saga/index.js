import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserExperience(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        }

        if (localStorage.getItem('experience')) {

            yield put({
                type: Actions.SAVE_USER_EXPERIENCE,
                data: {list: JSON.parse(localStorage.getItem('experience'))
                 || [{
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
                    }]}
                
            })
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserExperience, candidateId);
        if (result['error']) {
            ////console.log('error');
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
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
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}

function* updateUserExperience(action) {
    try {
        let {payload: {userExperience, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userExperience;

        const result = yield call(id ? Api.updateUserExperience : Api.createUserExperience, userExperience, candidateId, userExperience.id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('experience');

        yield put({type: Actions.SAVE_USER_EXPERIENCE, data: result['data']});

        return resolve('User Experience  Info saved successfully.');

    } catch (e) {
        ////console.log('error', e);
    }
}


function* bulkUserExperienceUpdate(action) {
    try {
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserExperience, list, candidateId);

        if (result['error']) {
            ////console.log(result['error']);
        }
        else{
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
        }

        ////console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        ////console.log('error', e);
    }
}


function* deleteUserExperience(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})

        const {experienceId} = action;

        const result = yield call(Api.deleteUserExperience, candidateId, experienceId);


        if (result['error']) {
            ////console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EXPERIENCE, id: experienceId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
        yield call(fetchUserExperience)
        

    } catch (e) {
        ////console.log('error', e);
    }
}

export default function* watchExperience() {
    yield takeLatest(Actions.FETCH_USER_EXPERIENCE, fetchUserExperience);
    yield takeLatest(Actions.UPDATE_USER_EXPERIENCE, updateUserExperience);
    yield takeLatest(Actions.DELETE_USER_EXPERIENCE, deleteUserExperience);
    yield takeLatest(Actions.BULK_UPDATE_USER_EXPERIENCE, bulkUserExperienceUpdate);
}