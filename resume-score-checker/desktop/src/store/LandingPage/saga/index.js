import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './API';
import {UPDATE_SCORE} from '../actions/actionTypes';
import { Toast } from '../../../services/Toast';

function* getCandidateId(action) {
    try {
        const { payload: { resolve} } = action;
        const result = yield call(Api.getCandidateId);

        localStorage.setItem('candidateId', JSON.parse((result.data && result.data['candidate_id'])) || '');
        resolve();

    } catch (e) {
        console.log(e);
    }
}




function* uploadFileUrl(action) {
    const { payload: { file1, resolve, reject } } = action; 
    try {  
        var fileData = new FormData();
        fileData.append('resume', file1)
        const result = yield call(Api.uploadFileUrl, fileData);
        if(result.data['error_message']){
            Toast.fire({
                icon: 'error',
                html : result.data.error_message
            })
            reject(result.data)
        }
        localStorage.setItem('resume_score',JSON.stringify({...result.data}))
        yield put({ type : UPDATE_SCORE, payload : result.data});
        return resolve(result)
    } catch (e) {
        
        return reject(e)
    }
}


function* expertFormSubmit(action) {
    const { payload: { data , resolve, reject } } = action;
    try {  
        let formData = data;
        formData['lsource'] = 8;

        const result = yield call(Api.expertFormSubmit, formData);
        return resolve(result)
 
    } catch (e) {
        return reject(e)
    }
}

function* checkSessionAvailability(action) {
    let { payload: { resolve } } = action;
    try {
       console.log("check session avail")
        let result = yield call(Api.checkSessionAvailability)
        if (result["error"]) {
            resolve(false)
        }
        const { data } = result;
        resolve(data['result']);
    } catch (e) {
        return resolve(false)
    }
}

function* getCandidateResume(action){
    const { payload: { resolve, reject } } = action; 
    try {  
        const result = yield call(Api.getCandidateResume);
        yield put({ type : UPDATE_SCORE, payload : { result }});
        return resolve(result)
    } catch (e) {
        return reject(e)
    }
}



export default function* watchlandingPage() {
    yield takeLatest(Actions.UPLOAD_FILE_URL, uploadFileUrl);
    yield takeLatest(Actions.EXPERT_FORM_SUBMIT, expertFormSubmit);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvailability);
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.GET_CANDIDATE_RESUME, getCandidateResume);
}