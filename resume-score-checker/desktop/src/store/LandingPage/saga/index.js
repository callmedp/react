import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import { Api } from './API';
import {UPDATE_SCORE} from '../actions/actionTypes';






function* uploadFileUrl(action) {
    try {
        const { payload: { file1, resolve } } = action;
        var fileData = new FormData();
        fileData.append('resume', file1)
        const result = yield call(Api.uploadFileUrl, fileData);
        yield put({ type : UPDATE_SCORE, payload : { result }});
        return resolve(result)
 
    } catch (e) {

        console.log('error', e);

    }
}


export default function* wathlandingPage() {
    yield takeLatest(Actions.UPLOAD_FILE_URL, uploadFileUrl);
}