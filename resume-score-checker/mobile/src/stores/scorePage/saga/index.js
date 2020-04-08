import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './Api';
import { UPDATE_SCORE } from '../actions/actionTypes';

function* fileUpload(action) {
    const { payload: { file, resolve, reject } } = action;
    try {
        var fileData = new FormData();
        fileData.append('resume', file);
        const result = yield call(Api.fileUpload, fileData);
        yield put({ type: UPDATE_SCORE, payload: { result }});
        return resolve(result)

    } catch (error) {
        return reject(error)
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
        localStorage.setItem('resume_score', localStorage.setItem("resume_score", JSON.stringify({response})))
        return resolve(response)
    }
    catch(e){
        console.log(e)
    }
}

function* getCandidateId(action) {
    let { payload: { resolve, reject } } = action;
    try {
        const result = yield call(Api.getCandidateId);
        localStorage.setItem('candidateId', JSON.parse((result.data && result.data['candidate_id'])) || '');
        return resolve(result)

    } catch (error) {
        reject(error)
    }
}

function* getCandidateResume(action) {
    let { payload: { resolve, reject } } = action;
    try{
        const resume = yield call(Api.getCandidateResume);
        return resolve(true)
    }
    catch (error) {
        return reject(error)
    }
}

function* checkSessionAvailability(action) {
    let { payload: { resolve, reject } } = action;
    try {
        let result = yield call(Api.checkSessionAvailability)
        if (result["error"]) {
            resolve(false)
        }
        const { data } = result;
        resolve(data['result']);
    } catch (e) {
        resolve(false)
    }
}

export default function* watchHomePage() {
    yield takeLatest(Actions.UPLOAD_FILE, fileUpload);
    yield takeLatest(Actions.SUBMIT_EXPERT_FORM, expertFormData);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvailability);
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.GET_CANDIDATE_RESUME, getCandidateResume);
}