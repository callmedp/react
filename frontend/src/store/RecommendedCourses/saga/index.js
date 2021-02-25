import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* getRecommendedProducts(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        const response = yield call(Api.getRecommendedData, payload);
        const item = response?.data;
        if (response["error"]) {
            return reject(response["error"])
        }
        yield put({ 
            type : Actions.RECOMMENDED_PRODUCTS_FETCHED, 
            item 
        })
        return resolve(item);

    } catch (e) {
        console.error("Exception occured at getRecommendedProducts",e)
        return reject(e);
    }
} 

export default function* WatchRecommendation(){
    yield takeLatest(Actions.FETCH_RECOMMENDED_PRODUCTS, getRecommendedProducts);
}