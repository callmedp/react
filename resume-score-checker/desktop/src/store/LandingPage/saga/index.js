import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './API';
import { UPDATE_SCORE } from '../actions/actionTypes';
import Swal from 'sweetalert2';

function* getCandidateId(action) {
    try {
        const { payload: { resolve } } = action;
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

        if (result.data['error_message']) {
            Swal.fire({
                icon: 'error',
                html: result.data.error_message
            })
            reject(result.data)
        }
        localStorage.setItem('resume_score', JSON.stringify({ ...result.data }))

        yield put({ type: UPDATE_SCORE, payload: result.data });
        return resolve(result)
    } catch (e) {

        return reject(e)
    }
}

function* getCandidateScore(action) {
    const { payload: { candidateId, resolve, reject } } = action;
    try {
        const result = yield call(Api.getCandidateScore, candidateId)
        if (result.data['error_message']) {
            Swal.fire({
                icon: 'error',
                html: result.data.error_message
            })
            return reject(result.data)
        }
        localStorage.setItem('resume_score', JSON.stringify({ ...result.data }))
        localStorage.setItem('file_name', "Imported from shine")
        yield put({ type: UPDATE_SCORE, payload: result.data });
        return resolve(result)
    }
    catch (e) {
        return reject(e)
    }
}

function* expertFormSubmit(action) {
    const { payload: { data, resolve, reject } } = action;
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
        let resp = yield call(Api.checkSessionAvailability)
        const { result } = resp;
        resolve({ result: result });
    } catch (e) {
        return resolve(false)
    }
}

function* getCandidateResume(action) {
    const { payload: { resolve, reject } } = action;
    try {
        const result = yield call(Api.getCandidateResume);
        yield put({ type: UPDATE_SCORE, payload: { result } });
        return resolve(result)
    } catch (e) {
        return reject(e);
    }
}

function* getCandidateInfo(action) {
    const { payload: { resolve, reject } } = action;
    try {
        const result = yield call(Api.getInformation);
        const { candidate_id, profile: { first_name, email } } = result;
        localStorage.setItem('userId', candidate_id);
        localStorage.setItem('userName', first_name);
        localStorage.setItem('userEmail', email);
        resolve({ candidateId: candidate_id || '', name: first_name || '', email: email || '' });
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



export default function* watchlandingPage() {
    yield takeLatest(Actions.UPLOAD_FILE_URL, uploadFileUrl);
    yield takeLatest(Actions.EXPERT_FORM_SUBMIT, expertFormSubmit);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvailability);
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.GET_CANDIDATE_RESUME, getCandidateResume);
    yield takeLatest(Actions.GET_CANDIDATE_SCORE, getCandidateScore);
    yield takeLatest(Actions.GET_CANDIDATE_INFO, getCandidateInfo);
    yield takeLatest(Actions.GET_CART_COUNT, getCartCount);

}