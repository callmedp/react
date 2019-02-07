import {Api} from './Api';
import {takeLatest, put, call, select} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';
import {SubmissionError} from 'redux-form'
import {UPDATE_USER_DETAILS} from "../actions/actionTypes";


function* saveUserInfo(action) {
    try {
        const {payload: {userDetails, resolve, reject}} = action;
        const result = yield call(Api.saveUserData, userDetails);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: result['data']});
        return resolve('Done');
    } catch (e) {
        console.log('error', e);
    }
}


function* updateUserInfo(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {userDetails, resolve, reject}} = action;
        userDetails = {
            ...userDetails,
            id: id
        }
        const result = yield call(Api.updateUserData, userDetails, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: result['data']});
        return resolve('Done');
    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchFetchHomeData() {
    yield takeLatest(Actions.SAVE_USER_DETAILS, saveUserInfo);
    yield takeLatest(Actions.UPDATE_USER_DETAILS, updateUserInfo);

}