import { takeLatest, call } from 'redux-saga/effects';
import Api from './Api';
import { logLearningTracking } from './actions';
import { addDefaultPayload } from 'utils/baseTracking';

function* learningTrackingWorker(action){

    const { payload: { payload } } = action;
    const superChargedPayload = addDefaultPayload(payload);
    yield call(Api.learningTrackingApi, superChargedPayload);

}

export default function* WatchLearningTracking() {
    yield takeLatest(logLearningTracking.type, learningTrackingWorker);
}
