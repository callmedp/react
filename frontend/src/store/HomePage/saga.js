import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { fetchShoppingList, shoppingListFetched } from './actions';




function* shopping(action){
    const { payload: { payload, resolve, reject} } = action;
    try{
    
        const response = yield call(Api.fetchShoppingList);
        console.log("response", response)
        if(response?.error){
            return reject(response);
        }
        
        yield put(shoppingListFetched({ item: response }))
        return resolve(response);
    }
    catch(e){
     
        return reject(e);
    }
}

export default function* WatchHomePage() {
    yield takeLatest(fetchShoppingList.type, shopping);

}
