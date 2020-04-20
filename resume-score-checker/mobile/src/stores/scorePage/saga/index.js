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
        
        if(!result.data['error_message']){
            yield put({ type: UPDATE_SCORE, payload: result.data });
            localStorage.setItem("resume_score", JSON.stringify({...result.data}))
        }
        return resolve(result.data)

    } catch (error) {
        return reject(error)
    }
}

function* expertFormData(action) {
    const { payload: {values, resolve, reject} } = action;
    try{
         let formData = values; 
        formData['lsource'] = 8;
        const response = yield call(Api.expertFormSubmit, formData);
        return resolve(response)
    }
    catch(error){
        return reject(error)
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
        yield call(Api.getCandidateResume);
        return resolve(true)
    }
    catch (error) {
        return reject(error)
    }
}

function* checkSessionAvailability(action) {
    let { payload: { resolve } } = action;
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