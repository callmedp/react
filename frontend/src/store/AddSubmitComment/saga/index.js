import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* oi_comment(action) {
    try {
        const { payload } = action;
        let result = null;

        if (payload.type === 'GET') result = yield call(Api.getOiComment, payload);
        else {
            result = yield call(Api.postOiComment, payload);
            if (!result["error"]) return yield put({ type: Actions.OI_COMMENT_FETCHED, comment : result.data });
            else return payload?.reject(result);
        }
        if (result["error"]) return payload?.reject(result);
        else return yield put({ type: Actions.OI_COMMENT_FETCHED, comment : result.data });
    }
    catch (e) {
        return e;
    }
}

export default function* WatchComments() {
    yield takeLatest(Actions.FETCH_OI_COMMENT, oi_comment);
}