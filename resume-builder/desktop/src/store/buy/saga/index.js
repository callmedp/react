import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'

import {Toast} from "../../../services/ErrorToast";

function* fetchProductIds(action) {
    try {
        const result = yield call(Api.fetchProductIds);
        if (result['error']) {
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
        }
        const {data: {results}} = result;
        yield put({type: Actions.SAVE_PRODUCT_IDS, data: results})
    } catch (e) {
        console.log(e);
    }
}

function* requestFreeResume(action) {
    try {
        const {payload: {resolve, reject}} = action
        const result = yield call(Api.requestFreeResume);
        console.log(result)

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        const {data: {results}} = result;
        console.log(results)
        
        return resolve(results)
    } catch (e) {
        console.log(e);
    }
}

function* pollingFreeResume(action) {
    try {
        const {payload: {resolve, reject}} = action
        const result = yield call(Api.pollingFreeResume);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        const {data: {poll_result}} = result;
        return resolve(poll_result)
    } catch (e) {
        console.log(e);
    }
}

function* downloadFreeResume(action) {
    try {
        const {payload: {resolve, reject}} = action
        const result = yield call(Api.downloadFreeResume);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        console.log(result)
        // const {data: {results}} = result;
        return resolve(result)
    } catch (e) {
        console.log(e);
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
        console.log(e);
    }
}

export default function* watchProductId() {
    yield takeLatest(Actions.GET_PRODUCT_IDS, fetchProductIds)
    yield takeLatest(Actions.ADD_TO_CART, addToCart)
    yield takeLatest(Actions.REQUEST_FREE_RESUME, requestFreeResume)
    yield takeLatest(Actions.POLLING_FREE_RESUME, pollingFreeResume)
    yield takeLatest(Actions.DOWNLOAD_FREE_RESUME, downloadFreeResume)

}