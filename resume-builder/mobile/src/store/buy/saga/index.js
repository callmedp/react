import { Api } from './Api';
import { apiError } from '../../../Utils/apiError';

import { takeLatest, put, call, select } from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import { SubmissionError } from 'redux-form'
import { siteDomain } from '../../../Utils/domains'
import { isTrackingInfoAvailable, getTrackingInfo } from '../../../Utils/common';

function* fetchProductIds(action) {
    try {
        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: true } })
        const result = yield call(Api.fetchProductIds);
        if (result['error']) {
            apiError();
        }
        const { data: { results } } = result;
        yield put({ type: Actions.SAVE_PRODUCT_IDS, data: results })
        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: false } })
    } catch (e) {
        apiError();
    }
}

function* addToCart(action) {
    try {
        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: true } })
        const { payload: { data, resolve, reject } } = action
        const result = yield call(Api.addToCart, data);
        if (result['error']) {
            apiError();
            yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: false } })
            return reject(new SubmissionError({ _error: result['errorMessage'] }));
        }
        else if (isTrackingInfoAvailable()) {
            const { trackingId, productId, triggerPoint, uId, utmCampaign, position } = getTrackingInfo()
            window.location.replace(`${siteDomain}/cart/payment-summary/?prod_id=${productId}&t_id=${trackingId}&trigger_point=${triggerPoint}&u_id=${uId}&utm_campaign=${utmCampaign}&position=${position}`)
        }
        else {
            window.location.replace(`${siteDomain}/cart/payment-summary/`)
        }
        return resolve('Product added to cart successfully.');


    } catch (e) {
        apiError();
    }
}

function* requestFreeResume(action) {
    try {
        const { payload: { resolve, reject } } = action
        const response = yield call(Api.requestFreeResume);

        if (response['error']) {
            return reject(new SubmissionError({ _error: response['errorMessage'] }));
        }

        const { data: { result } } = response;
        return resolve(result)
    } catch (e) {
        console.log(e);
    }
}

export default function* watchProductId() {
    yield takeLatest(Actions.GET_PRODUCT_IDS, fetchProductIds)
    yield takeLatest(Actions.ADD_TO_CART, addToCart)
    yield takeLatest(Actions.REQUEST_FREE_RESUME, requestFreeResume)
}