import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* DashboardOrdersApi(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.myOrdersData, payload);

        if (response["error"]) {
            return payload?.reject(response)
        }
        const item = response?.data?.data;

        yield put({ 
            type : Actions.MY_ORDERS_FETCHED, 
            item 
        })
        
        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured at Dashboard Api",e)
        return payload?.reject(e)
        
    }
}

function* CancelOrder(action) {
    const { payload : { payload, resolve, reject} } = action
    try {
        const response = yield call(Api.cancelOrder, payload);
        if (response?.error) {
            return resolve(response?.error)
        }
        const item = response?.data;

        // yield put({ 
        //     type : Actions.ORDER_CANCELLED, 
        //     item 
        // })
        
        return resolve(item);

    } catch (e) {
        console.error("Exception occured in Order Cancellation",e)
        return reject(e)
        
    }
}

export default function* WatchDashboardMyOrders() {
    yield takeLatest(Actions.FETCH_MY_ORDERS, DashboardOrdersApi);
    yield takeLatest(Actions.CANCEL_ORDER, CancelOrder)
}