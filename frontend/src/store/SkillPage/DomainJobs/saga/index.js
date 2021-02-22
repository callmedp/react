import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* domainJobs(action) {
    const { payload: { payload, resolve, reject } } = action;
    
    try {
   
        const response = yield call(Api.domainJobs, payload);
        
        if (response["error"]) {
            return reject(response)
        }
        
        const item = response.data;
        yield put({ 
            type : Actions.DOMAIN_JOBS_FETCHED, 
            item
        })
        return resolve(item);

    } catch (e) {
        console.error("Exception occured at domainJobs Api",e)
        return reject(e);
    }
}




export default function* WatchDomainJobs() {
    yield takeLatest(Actions.FETCH_DOMAIN_JOBS, domainJobs);
}