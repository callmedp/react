import { TRACK_USER } from '../actions/actionTypes';
import { call, takeEvery, put } from "redux-saga/effects"
import { Api } from './Api'


function* trackUser(action) {
    const { payload: { trackingId, productTrackingMappingId, productId, action: userAction, position,
        triggerPoint, uId, utmCampaign } } = action;
    try {
        yield call(Api.trackUser, trackingId, productTrackingMappingId, 
            productId, userAction, position, triggerPoint, uId, utmCampaign);
    }
    catch (e) {
    }
}





export default function* watchTracking() {
    yield takeEvery(TRACK_USER, trackUser)
}