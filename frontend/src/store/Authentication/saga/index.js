import * as Actions from '../actions/actionTypes';
import { takeLatest, call } from 'redux-saga/effects';
import Api from './Api';


function* fetchUserInfos(action) {
    const { payload: { payload, resolve, reject } } = action;

    try {
        const response = yield call(Api.fetchUserInform, payload);
        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data;
        sessionStorage.setItem('code2', item.code2 || 'IN');
        sessionStorage.setItem('candidate_id', item.candidate_id);
        return resolve(item)

    } catch (e) {
        return reject(e);
    }
}



export default function* WatchFetchUserInfo() {
    yield takeLatest(Actions.FETCH_USER, fetchUserInfos);
}