import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import {getCandidateId} from 'utils/storage';

function* DashboardServicesApi(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.myServicesData);

        if (response["error"]) {
            return payload?.reject(response)
        }
        const item = response.data;

        yield put({ 
            type : Actions.MY_SERVICES_FETCHED, 
            item 
        })
        
        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured at skillPageBanner Api",e)
        return payload?.reject(e)
        
    }
}

function* oi_comment(action) {
    try {
        const { payload } = action;
        let result = null;

        if (payload.type === 'GET') {
            result = yield call(Api.getOiComment, payload);
        }
        else {
            result = yield call(Api.postOiComment, payload);
            if (!result["error"]) {
                result = yield call(Api.getOiComment, payload);
                return yield put({ type: Actions.OI_COMMENT_SUCCESS, oi_comment: result.data });
            }
        }
        if (result["error"]) {
            return yield put({ type: Actions.OI_COMMENT_FAILED, error: 404 });
        }
        else {
            return yield put({ type: Actions.OI_COMMENT_SUCCESS, oi_comment: result.data });
        }
    }
    catch (e) {
        return yield put({ type: Actions.OI_COMMENT_FAILED, error: 500 });
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

function* submitFeedBack(action) {

    try {
        const { payload } = action;
        let result = null;

        result = yield call(Api.submitDashboardReviews, payload);
        if (result["error"]) {
            return yield put({ type: Actions.SUBMIT_DASHBOARD_FAILED, error: 'Something went wrong' });
        }
        else {
            return yield put({ type: Actions.SUBMIT_DASHBOARD_SUCCESS });
        }
    }
    catch (e) {
    }
}

export default function* WatchDashboardMyServices() {
    yield takeLatest(Actions.FETCH_MY_SERVICES, DashboardServicesApi);
    yield takeLatest(Actions.GET_OI_COMMENT, oi_comment);
    yield takeLatest(Actions.UPLOAD_RESUME_FORM, uploadResume);
    yield takeLatest(Actions.SUBMIT_DASHBOARD_REVIEWS, submitFeedBack);


}