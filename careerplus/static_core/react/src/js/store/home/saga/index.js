import {Api} from './Api';
import {takeLatest, put, call} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';
import {SubmissionError} from 'redux-form'


function* saveUserInfo(action) {
    try {
        const {payload: {userDetails, resolve, reject}} = action;
        const result = yield call(Api.saveUserData, userDetails);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.SAVE_USER_DETAILS, data: result['data']});
        return resolve('Done');
    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchFetchHomeData() {
    yield takeLatest(Actions.SAVE_USER_DETAILS, saveUserInfo);

}