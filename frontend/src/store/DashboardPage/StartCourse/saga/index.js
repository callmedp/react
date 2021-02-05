import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* getVendorUrl(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        const response = yield call(Api.getCourseURL, payload);
        return resolve(response.data)
    }
    catch (error) {
        debugger;
        return reject(error)
    }
}

export default function* WatchDashboardStartCourse() {
    yield takeLatest(Actions.GET_VENDOR_URL, getVendorUrl);
}