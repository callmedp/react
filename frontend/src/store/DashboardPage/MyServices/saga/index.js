import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { getCandidateId } from 'utils/storage';
import Swal from 'sweetalert2';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';

function* DashboardServicesApi(action) {
    const { payload } = action;
    try {

        const response = yield call(Api.myServicesData, payload);

        if (response["error"]) {
            return payload?.reject(response)
        }
        let item = response?.data?.data;

        yield put({
            type: Actions.MY_SERVICES_FETCHED,
            item
        })

        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured at My service Api", e)
        return payload?.reject(e)

    }
}

function* getPendingOrder(action) {
    const { payload: { resolve, reject } } = action;

    try {
        const result = yield call(Api.getPendingOrderItems);

        let data = result?.data?.data;

        yield put({
            type: Actions.PENDING_RESUME_FETCHED,
            data
        })
        return resolve(data);
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
                icon: 'error',
                html: result.errorMessage
            })
            return reject()
        }
        else {
            yield put({ type: Actions.CANDIDATE_OI_ACCEPT_REJECT_SUCCESS, result });
            // Swal.fire({
            //     icon: 'success',
            //     title: 'Reject Request Sent!'
            // })
            return resolve()
        }
    }
    catch (e) {
        Swal.fire({
            icon: 'error',
            html: "<h3>Something went wrong.</h3>"
        })
        return reject()
    }

}

function* pauseResumeService(action) {
    try {
        const { payload } = action;
        const oi_status = payload?.oi_status
        yield put(startDashboardServicesPageLoader());
        const result = yield call(Api.pauseResumeService, payload);
        yield put(stopDashboardServicesPageLoader());
        if (result["error"]) {
            Swal.fire({
                icon : 'error',
                html : 'Something went wrong!'
            })
            return result
            
        }
        const item = result?.data?.oi_status
        const error = item !== oi_status ? true : false
        Swal.fire({
            icon: error ? 'error' : 'success',
            title: error ? `Please wait 24 hours before ${ oi_status === 34 ? 'pausing' : 'resuming'} ` : 
                    item ===34 ? 'Service is Paused' : 'Service is Resumed'
        })
        return yield put({ type: Actions.PAUSE_AND_RESUME_SERVICE_SUCCESS, oi: result.data });
    }
    catch (e) {
        yield put(stopDashboardServicesPageLoader());
        return e

    }

}

function* fetchOiDetails(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        const result = yield call(Api.fetchOiDetailsApi, payload);

        if (result["error"]) {
            return resolve(result)

        }
        const item = result?.data

        yield put({ type: Actions.OI_DETAILS_FETCHED, item });
        return resolve(result?.data)
    }
    catch (e) {
        return resolve(e)
    }

}

function* updateResume(action) {
    const { payload: { updatedValue, resolve, reject } } = action;
    try {
        const response = yield call(Api.updateResumeShineApi, updatedValue);
        return resolve(response)
    }
    catch (error) {
        return reject(error)
    }
}
export default function* WatchDashboardMyServices() {
    yield takeLatest(Actions.FETCH_MY_SERVICES, DashboardServicesApi);
    yield takeLatest(Actions.UPLOAD_RESUME_FORM, uploadResume);
    yield takeLatest(Actions.GET_PENDING_RESUME, getPendingOrder);
    yield takeLatest(Actions.REQUEST_CANDIDATE_OI_ACCEPT_REJECT, acceptrejectcandidate);
    yield takeLatest(Actions.PAUSE_AND_RESUME_SERVICE_REQUEST, pauseResumeService);
    yield takeLatest(Actions.FETCH_OI_DETAILS, fetchOiDetails);
    yield takeLatest(Actions.UPDATE_RESUME_SHINE, updateResume);

}