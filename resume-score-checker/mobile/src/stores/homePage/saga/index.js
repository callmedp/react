import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './Api';
import { UPDATE_SCORE } from '../actions/actionTypes';

function* fileUpload(action) {
    try {
        const { payload: { file, resolve } } = action;
        var fileData = new FormData();
        fileData.append('resume', file);
        const result = yield call(Api.fileUpload, fileData);
        yield put({ type: UPDATE_SCORE, payload: { result }});
        return resolve(result)

    } catch (e) {

        console.log('error', e);
    }
}

export default function* watchHomePage() {
    yield takeLatest(Actions.UPLOAD_FILE, fileUpload);
}