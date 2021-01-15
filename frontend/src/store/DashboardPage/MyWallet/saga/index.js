import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* DashboardWalletApi(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.myWalletData, payload);

        if (response["error"]) {
            return payload?.reject(response)
        }
        const item = response.data;

        //converts 1D array to 2D array if medium is Desktop
        // if(!!payload && !payload.medium && !!item && item.testimonialCategory instanceof Array){
        //     const storiesList = item?.testimonialCategory.reduce((rows, key, index) => 
        //         (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
            
        //     if(storiesList.length){
        //         item.testimonialCategory = storiesList.slice()
        //     }
        // }

        yield put({ 
            type : Actions.MY_WALLET_FETCHED, 
            item 
        })
        
        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured at skillPageBanner Api",e)
        return payload?.reject(e)
        
    }
}

export default function* WatchDashboardMyWallet() {
    yield takeLatest(Actions.FETCH_MY_WALLET, DashboardWalletApi);
}