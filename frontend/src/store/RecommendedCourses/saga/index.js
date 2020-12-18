import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* getRecommendedProducts(action) {
    try {
        const { payload } = action;
        const response = yield call(Api.getRecommendedData, payload);
        const item = response?.data;

        yield put({ 
            type : Actions.RECOMMENDED_PRODUCTS_FETCHED, 
            item 
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}

export default function* WatchRecommendation(){
    yield takeLatest(Actions.FETCH_RECOMMENDED_PRODUCTS, getRecommendedProducts);
}