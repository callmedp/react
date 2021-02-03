import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {getCandidateId} from 'utils/storage';
import Swal from 'sweetalert2';

function* DashboardServicesApi(action) {
    const { payload } = action;
    try {
       
        const response = yield call(Api.myServicesData, payload);
     
        if (response["error"]) {
            return payload?.reject(response)
        }
        let item = response?.data?.data;

        yield put({ 
            type : Actions.MY_SERVICES_FETCHED, 
            item 
        })

        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured at My service Api",e)
        return payload?.reject(e)
        
    }
}

function* getPendingOrder(action) {
    const { payload: { resolve, reject } } = action;

    try {
        const result = yield call(Api.getPendingOrderItems);
        return resolve({ type: Actions.PENDING_RESUME_FETCHED, data: result?.data?.data });
    }
    catch (e) {
        return reject(e);
    }
}

function* uploadResume(action) {
    const { payload: { values, resolve, reject } } = action;
    try {
        let formData = new FormData();
        formData.append('file', values.file);
        formData.append('resume_shine', values.shine_resume ? values.shine_resume : '');
        formData.append('resume_pending', values.resume_course);
        formData.append('candidate_id', getCandidateId());
        
        const response = yield call(Api.uploadResumeDashboardForm, formData);
        return resolve(response)
    }
    catch (error) {
        return reject(error)
    }
}

function* acceptrejectcandidate(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        let result = undefined

        if (payload.type === 'accept') {
            result = yield call(Api.candidateAccept, payload);
        }
        else {
            let formData = new FormData();
            formData.append('reject_file', payload.file);
            formData.append('comment', payload.message);
            formData.append('oi_pk', payload.oi);
            result = yield call(Api.candidateReject, formData);
        }

        if (result["error"]) {
            Swal.fire({
                icon : 'error',
                html : result.errorMessage
            })
            return reject()
        }
        else {
            yield put({ type: Actions.CANDIDATE_OI_ACCEPT_REJECT_SUCCESS, result });
            Swal.fire({
                icon: 'success',
                title: 'Reject Request Sent!'
            })
            return resolve()
        }
    }
    catch (e) {
        Swal.fire({
            icon : 'error',
            html : "<h3>Something went wrong.</h3>"
        })
        return reject()
    }

}

function* pauseResumeService(action) {
    try {
        const { payload } = action;
        const result = yield call(Api.pauseResumeService, payload);
        
        if (result["error"]) {
            return result
            
        }
        return yield put({ type: Actions.PAUSE_AND_RESUME_SERVICE_SUCCESS, oi: result.data });
    }
    catch (e) {
        return e
        
    }
    
}

export default function* WatchDashboardMyServices() {
    yield takeLatest(Actions.FETCH_MY_SERVICES, DashboardServicesApi);
    yield takeLatest(Actions.UPLOAD_RESUME_FORM, uploadResume);
    yield takeLatest(Actions.GET_PENDING_RESUME, getPendingOrder);
    yield takeLatest(Actions.REQUEST_CANDIDATE_OI_ACCEPT_REJECT, acceptrejectcandidate);
    yield takeLatest(Actions.PAUSE_AND_RESUME_SERVICE_REQUEST, pauseResumeService);
}