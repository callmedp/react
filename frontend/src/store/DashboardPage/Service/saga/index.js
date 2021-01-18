import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* recentAddedServices(action) {
    const { payload } = action;

    try {
        const response = yield call(Api.recentAddedServices);

        if(!response || response?.error) {
            return payload?.reject(response?.error)
        }
        const item = response.data;
        console.log(item)
        yield put({
            type: Actions.FETCHED_ALL_SERVICES,
            item
        })
        return payload?.resolve(item)
    }
    catch(e){
        console.error("Exception occured in recentlyAddedServices Api", e)
        return payload?.reject(e);
    }
}


export default function* WatchServicePage() {
    yield takeLatest(Actions.FETCHING_ALL_SERVICES, recentAddedServices);
}