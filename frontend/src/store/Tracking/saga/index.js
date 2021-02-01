import { TRACK_USER } from '../actions/actionTypes';
import { call, takeEvery, put } from "redux-saga/effects"
import { Api } from './Api'


function* trackUser(action) {
    const { payload: { query, action: userAction }} = action;
    try {
        yield call(Api.trackUser, query, userAction);
        //yield call(Api.trackUser, trackingId, productTrackingMappingId, productId, userAction, position, triggerPoint, uId, utmCampaign, popup_based_product );        
    }
    catch (e) {
        console.error("Exception occured at trackuser Api", e);
    }
}

export default function* watchTracking() {
    yield takeEvery(TRACK_USER, trackUser)
}