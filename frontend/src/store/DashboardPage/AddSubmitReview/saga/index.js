import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

// fetch and submit reviews
function* Reviews(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        let result = null;

        if (payload.type === 'GET'){
            result = yield call(Api.myReviewsData, payload);

            if (result["error"]) return resolve(result.data);
            else{
                yield put({ type: Actions.REVIEWS_FETCHED, reviews: result?.data?.data });
                return resolve(result)
            }
        }
        else {
            result = yield call(Api.saveReviewsData, {'rating': payload.rating, 'review': payload.review, 'title': payload.title, 'oi_pk': payload.oi_pk, 'full_name' : payload.full_name});
            if (!result["error"]){
                yield put({ type: Actions.REVIEWS_FETCHED, reviews: result?.data?.data });
            }
            return resolve(result)
        }

    }
    catch (e) {
        return e;
    }
}

export default function* WatchReviews() {
    yield takeLatest(Actions.FETCH_REVIEWS, Reviews);
}