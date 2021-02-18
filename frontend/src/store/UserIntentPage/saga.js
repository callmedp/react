import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { fetchedUserIntentData } from './actions';

function* userIntentData(action) {
    const { payload } = action;
    
    try {
        const response = yield call(Api.userIntentData, payload);

        if (response?.error) {
            return payload?.reject(response?.error);
        }
        const item = response?.data.data;
        yield put(fetchedUserIntentData({ [payload.categoryId]: item.mostViewCourses }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.error("Exception occured in userIntent data", e);
        return payload?.resolve(e);

    }
}

export default function* WatchUserIntentPage() {
    yield takeLatest(fetchedUserIntentData.type, userIntentData);
}