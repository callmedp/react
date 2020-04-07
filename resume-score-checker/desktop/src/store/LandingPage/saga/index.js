import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './API';
import {UPDATE_SCORE} from '../actions/actionTypes';






function* uploadFileUrl(action) {
    const { payload: { file1, resolve, reject } } = action;
    try {  
        var fileData = new FormData();
        fileData.append('resume', file1)
        const result = yield call(Api.uploadFileUrl, fileData);
        yield put({ type : UPDATE_SCORE, payload : { result }});
        return resolve(result)
 
    } catch (e) {
        return reject(e)
    }
}


function* expertFormSubmit(action) {
    const { payload: { data , resolve, reject } } = action;
    try {  
        let formData = new FormData();
        formData.append('resume', data)
        const result = yield call(Api.expertFormSubmit, formData);
        return resolve(result)
 
    } catch (e) {
        return reject(e)
    }
}

function* checkSessionAvaialability(action) {
    let { payload: { resolve, reject } } = action;
    try {
       
        let result = yield call(Api.checkSessionAvaialability)
        if (result["error"]) {
            resolve(false)
        }
        const { data } = result;
        resolve(data['result']);
    } catch (e) {
        throw reject(e)
    }
}



export default function* watchlandingPage() {
    yield takeLatest(Actions.UPLOAD_FILE_URL, uploadFileUrl);
    yield takeLatest(Actions.EXPERT_FORM_SUBMIT, expertFormSubmit);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvaialability);
}