import { takeLatest, call } from 'redux-saga/effects';
import Api from './Api';
import { logLearningTracking } from './actions';
import { addDefaultPayload } from 'utils/baseTracking';

function* learningTrackingWorker(action){
    console.log("learning tracking actions", action)
    const { payload } = action;
    console.log("learning tracking payload", payload)
    const superChargedPayload = addDefaultPayload(payload);
    yield call(Api.learningTrackingApi, superChargedPayload);

}

export default function* WatchLearningTracking() {
    yield takeLatest(logLearningTracking.type, learningTrackingWorker);
}
