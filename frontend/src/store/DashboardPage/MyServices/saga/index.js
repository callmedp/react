import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {getCandidateId} from 'utils/storage';

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



export default function* WatchDashboardMyServices() {
    yield takeLatest(Actions.FETCH_MY_SERVICES, DashboardServicesApi);
    yield takeLatest(Actions.UPLOAD_RESUME_FORM, uploadResume);


}