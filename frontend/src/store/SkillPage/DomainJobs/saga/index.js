import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* domainJobs(action) {
    try {
        const { payload } = action;

        const response = yield call(Api.domainJobs, payload);

        if (response["error"]) {
            return
        }
        
        const item = response.data;
        yield put({ 
            type : Actions.DOMAIN_JOBS_FETCHED, 
            item
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchDomainJobs() {
    yield takeLatest(Actions.FETCH_DOMAIN_JOBS, domainJobs);
}