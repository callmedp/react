import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './Api';
import { UPDATE_SCORE } from '../actions/actionTypes';

function* fileUpload(action) {
    try {
        const { payload: { file, resolve } } = action;
        var fileData = new FormData();
        fileData.append('resume', file);
        const result = yield call(Api.fileUpload, fileData);
        yield put({ type: UPDATE_SCORE, payload: { result }});
        return resolve(result)

    } catch (e) {

        console.log('error', e);
    }
}

function* expertFormData(action) {
    try{
        const { payload: {values, resolve} } = action;
        var formData = new FormData();
        formData.append('name', values.name);
        formData.append('email', values.email);
        formData.append('country_code', values.country_code);
        formData.append('mobile', values.mobile);
        const response = yield call(Api.expertFormSubmit, formData);
        return resolve(response)
    }
    catch(e){
        console.log(e)
    }
}

function* importShineResume(action) {
    try{
        const {payload : {candidateId, resolve, reject} } = action;
        const result = yield call(Api.importShineResume, candidateId)
        return resolve(result)

    } catch(e){
        console.log(e)
    }
}

function* getCandidateId() {
    try {
        const result = yield call(Api.getCandidateId);

        localStorage.setItem('candidateId', JSON.parse((result.data && result.data['candidate_id'])) || '');

    } catch (e) {
        console.log(e)
    }
}

function* checkSessionAvailability(action) {
    try {
        let { payload: { resolve, reject } } = action;
        let result = yield call(Api.checkSessionAvailability)
        if (result["error"]) {
            resolve(false)
        }
        const { data } = result;
        resolve(data['result']);
    } catch (e) {
        console.log(e);
    }
}

export default function* watchHomePage() {
    yield takeLatest(Actions.UPLOAD_FILE, fileUpload);
    yield takeLatest(Actions.SUBMIT_EXPERT_FORM, expertFormData);
    yield takeLatest(Actions.IMPORT_SHINE_RESUME, importShineResume);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvailability);
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
}