import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* DashboardCoursesApi(action) {
    const { payload } = action;
    try {

        const response = yield call(Api.myCoursesData, payload);

        if (response["error"]) {
            return payload?.reject(response)
        }
        console.log(response.data.data)
        const item = response?.data?.data;
        yield put({ 
            type : Actions.MY_COURSES_FETCHED, 
            item 
        })
        
        return payload?.resolve(item);

    } catch (e) {
        console.error("Exception occured at Dashboard Api",e)
        return payload?.reject(e)
        
    }
}

function* submitBoardNeoUser(action) {
    const { payload: { values, resolve, reject } } = action;
    try {
        const response = yield call(Api.boardNeoUser, values);
        return resolve(response)
    }
    catch (error) {
        return reject(error)
    }
}

export default function* WatchDashboardMyOrders() {
    yield takeLatest(Actions.FETCH_MY_COURSES, DashboardCoursesApi);
    yield takeLatest(Actions.BOARD_NEO_USER, submitBoardNeoUser);
}