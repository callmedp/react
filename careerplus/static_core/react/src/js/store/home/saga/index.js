import {Api} from './Api';
import {takeLatest, takeEvery, put, call} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';


function* fetchHome() {
    try {
        console.log('0000c --- sagas');
        const homeData = yield call(Api.fetchHomeData);
        yield put({type: Actions.SAVE_HOME_DATA, data: homeData});
    } catch (e) {
        console.log('--the error is here---', e);
    }
}

//
// function* saveHome(action) {
//     try {
//         console.log('----in herer', action);
//         const response = yield call(Api.saveHomeData);
//         console.log('-----', response);
//     } catch (e) {
//
//     }
// }

export default function* watchFetchHomeData() {
    console.log('00herre');
    yield takeEvery(Actions.FETCH_HOME_DATA, fetchHome);
}