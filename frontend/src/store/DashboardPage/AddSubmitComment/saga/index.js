import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* oi_comment(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        let result = null;

        if (payload.type === 'GET') result = yield call(Api.getOiComment, payload);
        else {
            result = yield call(Api.postOiComment, payload);
            if (!result["error"]){
                yield put({ type: Actions.OI_COMMENT_FETCHED, comment : result.data });
                return resolve(result?.data)
            }
            else return resolve(result);
        }
        if (result["error"]) return resolve(result);
        else{
            yield put({ type: Actions.OI_COMMENT_FETCHED, comment : result.data });
            return resolve(result?.data)
        }
    }
    catch (e) {
        return reject('Something went wrong');
    }
}

export default function* WatchComments() {
    yield takeLatest(Actions.FETCH_OI_COMMENT, oi_comment);
}