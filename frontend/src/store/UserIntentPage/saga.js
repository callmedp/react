import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { fetchedUserIntentData, fetchCareerChangeData, careerChangeDataFetched, fetchFindRightJobsData, findRightJobsDataFetched, fetchUpskillYourselfData, upskillYourselfDataFetched } from './actions';

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

function* careerChangeData(action) {
    const { payload } = action;
    
    try {
        const response = yield call(Api.careerChangeData);
        if (response?.error) {
            return payload?.resolve(response.error)
        }
        const item = response?.data;
        yield put(careerChangeDataFetched({ ...item }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.error("Exception occured in userIntent data", e);
        return payload?.resolve(e);

    }
}

function* findJobsData(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.findRightJobsData, payload.data);

        if (response?.error) return payload?.reject(response?.error);

        const item = response?.data.data;
        yield put(findRightJobsDataFetched({ ...item }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.error("Exception occured in userIntent data", e);
        return payload?.resolve(e);
    }
}

function* upskillData(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.upskillYourselfData, payload.dataUpskill);

        if (response?.error) return payload?.reject(response?.error);

        const item = response?.data.data;
        yield put(upskillYourselfDataFetched({ ...item }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.error("Exception occured in userIntent data", e);
        return payload?.resolve(e);
    }
}

export default function* WatchUserIntentPage() {
    yield takeLatest(fetchedUserIntentData.type, userIntentData);
    yield takeLatest(fetchCareerChangeData.type, careerChangeData);
    yield takeLatest(fetchFindRightJobsData.type, findJobsData);
    yield takeLatest(fetchUpskillYourselfData.type, upskillData);
}