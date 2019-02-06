import {Api} from './Api';
import {takeLatest, put, call} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';


function* fetchHome() {
    try {
        console.log('0000c --- sagas');
        const homeData = yield call(Api.fetchHomeData);
        yield put({type: Actions.SAVE_HOME_DATA, data: homeData});
    } catch (e) {
        console.log('error', e);
    }
}


function* saveUserInfo(action) {
    try {
        const {payload: {userDetails, resolve, reject}} = action;
        const result = yield call(Api.saveUserData, userDetails);
        resolve();
    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchFetchHomeData() {
    yield takeLatest(Actions.FETCH_HOME_DATA, fetchHome);
    yield takeLatest(Actions.SAVE_USER_DETAILS, saveUserInfo);

}