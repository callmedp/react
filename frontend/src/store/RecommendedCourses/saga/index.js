import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* getRecommendedProducts(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.getRecommendedData, payload);
        const item = response?.data;
        if (response["error"]) {
            return payload?.reject(response["error"])
        }
        yield put({ 
            type : Actions.RECOMMENDED_PRODUCTS_FETCHED, 
            item 
        })
        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured ",e)
        return payload?.reject(e);
    }
} 

export default function* WatchRecommendation(){
    yield takeLatest(Actions.FETCH_RECOMMENDED_PRODUCTS, getRecommendedProducts);
}