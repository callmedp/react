import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

// fetch and submit reviews
function* GetReviews(action) {
    try {
        const { payload } = action;
        let result = null;

        result = yield call(Api.myReviewsData, payload);
        // else {
        //     result = yield call(Api.saveReviewsData, {'rating': payload.rating, 'review': payload.review, 'title': payload.title, 'oi_pk': payload.oi_pk, 'full_name' : payload.full_name});
        //     if (!result["error"]) yield put({ type: Actions.REVIEWS_FETCHED, reviews: result });
        // }
        console.log(result);
        if (result["error"]) return payload?.reject(result.data);
        else return yield put({ type: Actions.REVIEWS_FETCHED, reviews: result.data.data });
    }
    catch (e) {
        return e;
    }
}

function* SubmitReview(action) {
    const { payload: { new_review, resolve, reject } } = action;
    console.log(action);
    try {
        const response = yield call(Api.saveReviewsData, new_review);

        if(response['error']) return reject(response.data)
        return resolve(response.data)
    }
    catch (error) {
        return reject(error)
    }
}

export default function* WatchReviews() {
    yield takeLatest(Actions.FETCH_REVIEWS, GetReviews);
    yield takeLatest(Actions.REVIEW_SUBMIT, SubmitReview);
}