import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

// fetch and submit reviews
function* GetReviews(action) {

    const { payload: { payload, resolve, reject } } = action;
    console.log(payload);
    try {
        let result = null;

        result = yield call(Api.myReviewsData, payload);
        
        if (result["error"]){
            yield put({ type: Actions.REVIEWS_FETCHED, reviews: result?.data?.data });
            return resolve(result?.data);
        } 
        else{
            yield put({ type: Actions.REVIEWS_FETCHED, reviews: result?.data?.data });
            return resolve(result)
        }
    }
    catch (e) {
        return resolve(e);
    }

}

function* SubmitReview(action) {
    const { payload: { payload, resolve, reject } } = action;

    try {
        const response = yield call(Api.saveReviewsData, payload);

        if(response['error']) return resolve(response)

        return resolve(response)
    }
    catch (error) {
        return resolve(error)
    }
}

export default function* WatchReviews() {
    yield takeLatest(Actions.FETCH_REVIEWS, GetReviews);
    yield takeLatest(Actions.REVIEW_SUBMIT, SubmitReview);
}