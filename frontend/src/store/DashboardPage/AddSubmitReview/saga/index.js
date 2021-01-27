import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

// fetch and submit reviews
function* Reviews(action) {
    try {
        const { payload } = action;
        let result = null;

        if (payload.type === 'GET') result = yield call(Api.myReviewsData, payload);
        else {
            result = yield call(Api.saveReviewsData, {'rating': payload.rating, 'review': payload.review, 'title': payload.title, 'oi_pk': payload.oi_pk, 'full_name' : payload.full_name});
            if (!result["error"]) yield put({ type: Actions.REVIEWS_FETCHED, reviews: result });
        }

        if (result["error"]) return payload?.reject(result.data);
        else return yield put({ type: Actions.REVIEWS_FETCHED, reviews: result.data.data });
    }
    catch (e) {
        return e;
    }
}

export default function* WatchReviews() {
    yield takeLatest(Actions.FETCH_REVIEWS, Reviews);
}