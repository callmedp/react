import {Api} from './Api';
import {apiError} from '../../../Utils/apiError';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import {SubmissionError} from 'redux-form'
import {siteDomain} from '../../../Utils/domains'


function* fetchProductIds(action) {
    try {
        yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: true}})
        const result = yield call(Api.fetchProductIds);
        if (result['error']) {
            apiError();
        }
        const {data: {results}} = result;
        yield put({type: Actions.SAVE_PRODUCT_IDS, data: results})
        yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: false}})
    } catch (e) {
        apiError();
    }
}

function* addToCart(action) {
    try {
        yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: true}})
        const {payload: {data, resolve, reject}} = action
        const result = yield call(Api.addToCart, data);
        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            window.location.href = `${siteDomain}/cart/payment-summary/`
        }
        yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: false}})
        return resolve('Product added to cart successfully.');


    } catch (e) {
        apiError();
    }
}

export default function* watchProductId() {
    yield takeLatest(Actions.GET_PRODUCT_IDS, fetchProductIds)
    yield takeLatest(Actions.ADD_TO_CART, addToCart)
}