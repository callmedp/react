import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchUserExperience(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        if (localStorage.getItem('experience')) {

            yield put({
                type: Actions.SAVE_USER_EXPERIENCE,
                data: {list: JSON.parse(localStorage.getItem('experience')) || []}
            })
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
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserExperience, list, candidateId);

        if (result['error']) {
            ////console.log(result['error']);
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

        const {experienceId} = action;

        const result = yield call(Api.deleteUserExperience, candidateId, experienceId);


        if (result['error']) {
            ////console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EXPERIENCE, id: experienceId});
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