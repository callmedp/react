import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { fetchLeadManagement, leadManagementFetched } from './actions';

function* mostViewedCourse(action){
    const { payload: { payload, resolve, reject } } = action;
    try {
        const response = yield call(Api.leadManagementApi, payload);
        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data;

        yield put(leadManagementFetched({ ...item }))
        return resolve(item)

    } catch (e) {
        return reject(e);
    }
}

export default function* WatchHomePage() {
    yield takeLatest(fetchLeadManagement.type, mostViewedCourse);
}
