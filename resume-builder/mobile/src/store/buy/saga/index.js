import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'


function* fetchProductIds(action) {
    try {
        const result = yield call(Api.fetchProductIds);
        if (result['error']) {
            ////console.log('error');
        }
        const {data: {results}} = result;
        yield put({type: Actions.SAVE_PRODUCT_IDS, data: results})
    } catch (e) {
        ////console.log(e);
    }
}

function* addToCart(action) {
    try {
        const {payload: {data, resolve, reject}} = action
        const result = yield call(Api.addToCart, data);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        return resolve('Product added to cart successfully.');

    } catch (e) {
        ////console.log(e);
    }
}

export default function* watchProductId() {
    yield takeLatest(Actions.GET_PRODUCT_IDS, fetchProductIds)
    yield takeLatest(Actions.ADD_TO_CART, addToCart)
}