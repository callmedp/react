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

        // const result = yield call(Api.getPendingOrderItems);


        // // console.log(result?.data?.data)
        // let modifiedData = {
        //     ...item,
        //     ...{
        //         'pending_resume_items': result.data.data.pending_resume_items ? result.data.data.pending_resume_items : []
        //     }
        // }

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
    const { payload : { payload, resolve, reject } } = action;
    try {
        let result = null;

        if (payload.type === 'GET') {
            result = yield call(Api.getOiComment, payload);
        }
        else {
            result = yield call(Api.postOiComment, payload);
            if (!result["error"]) {
                return resolve(result);
            }
        }
        if (result["error"]) {
            yield put({ type: Actions.OI_COMMENT_FAILED, error: 404 });
            return resolve(result);
        }
        else {
            yield put({ type: Actions.OI_COMMENT_SUCCESS, oi_comment: result.data });
            return resolve(result);
        }
    }
    catch (e) {
        yield put({ type: Actions.OI_COMMENT_FAILED, error: 500 });
        return resolve({
            message:'Something went wrong',
            error: true
        })
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

// fetch and submit reviews
function* reviews(action) {
    try {
        const { payload } = action;
        let result = null;

        if (payload.type === 'GET') {
            result = yield call(Api.myReviewsData, payload);
        }
        else {
            result = yield call(Api.saveReviewsData, {'rating': payload.rating, 'review': payload.review, 'title': payload.title});
            if (!result["error"]) {
                return payload?.resolve(result);
            }
        }
        if (result["error"]) {
            return yield put({ type: Actions.SUBMIT_DASHBOARD_FAILED, error: 404 });
        }
        else {
            return yield put({ type: Actions.SUBMIT_DASHBOARD_SUCCESS, reviews: result.data });
        }
    }
    catch (e) {
        return yield put({ type: Actions.SUBMIT_DASHBOARD_FAILED, error: 500 });
    }
}

function* getPendingResume(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.getPendingResumes, payload);

        if (response["error"]) {
            return payload?.resolve(response);
        }
        const item = response?.data?.data
        yield put({
            type: Actions.PENDING_RESUMES_FETCHED,
            item
        })
        return payload?.resolve(response);
    }
    catch (e) {
        return payload?.resolve('Something went wrong!');
    }
}

export default function* WatchDashboardMyServices() {
    yield takeLatest(Actions.FETCH_MY_SERVICES, DashboardServicesApi);
    yield takeLatest(Actions.GET_OI_COMMENT, oi_comment);
    yield takeLatest(Actions.UPLOAD_RESUME_FORM, uploadResume);
    yield takeLatest(Actions.FETCH_MY_REVIEWS, reviews);
    yield takeLatest(Actions.FETCH_PENDING_RESUMES, getPendingResume)
}