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
        let resp = yield call(Api.checkSessionAvailability)
        if (resp["error"]) {
            resolve({result:false})
        }
        const { result } = resp;
        resolve({result: result});
    } catch (e) {
            resolve({result:false})
    }
}


function* getCandidateScore(action) {
    const { payload: { candidateId, resolve, reject } } = action;
    try {
        const result = yield call(Api.getCandidateScore, candidateId)
        if(!result.data['error_message']){
            yield put({ type: UPDATE_SCORE, payload: result.data });
            localStorage.setItem("resume_score", JSON.stringify({...result.data}))
        }
        return resolve(result.data)
    }
    catch (e) {
        return reject(e)
    }
}

function* getCandidateInfo(action) {
    const { payload: { resolve, reject }} = action;
    try {
        const result = yield call(Api.getInformation);
        const {candidate_id, profile:{first_name, email}} = result; 
        localStorage.setItem('userId', candidate_id);
        localStorage.setItem('userName', first_name);
        localStorage.setItem('userEmail', email);
        resolve({candidateId:candidate_id|| '', name: first_name||'', email:email|| ''});
    }
    catch (e) {
        return reject(e);
    }
}



function* getCartCount(action) {
    try {
        const result = yield call(Api.getCartCount);
        const { count } = result;
        yield put({ type: UPDATE_SCORE, payload: { cartCount: count }});

    }
    catch (e) {
        // handle cart error in future.
    }
}



export default function* watchHomePage() {
    yield takeLatest(Actions.UPLOAD_FILE, fileUpload);
    yield takeLatest(Actions.SUBMIT_EXPERT_FORM, expertFormData);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvailability);
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.GET_CANDIDATE_RESUME, getCandidateResume);
    yield takeLatest(Actions.GET_CANDIDATE_SCORE, getCandidateScore);
    yield takeLatest(Actions.GET_CANDIDATE_INFO, getCandidateInfo);
    yield takeLatest(Actions.GET_CART_COUNT, getCartCount);


}