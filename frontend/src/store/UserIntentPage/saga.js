import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { fetchedUserIntentData, fetchFindRightJobsData, findRightJobsDataFetched, fetchUpskillYourselfData, upskillYourselfDataFetched, uploadFileUrl, fetchServiceRecommendation, serviceRecommendationFetched, sendFeedback } from './actions';

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

function* findJobsData(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.findRightJobsData, payload);

        if (response?.error) return payload?.reject(response?.error);

        const item = response?.data?.data;
        item.jobsList = item?.jobsList ?? {};
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

        const item = response?.data?.data;
        yield put(upskillYourselfDataFetched({ ...item }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.error("Exception occured in userIntent data", e);
        return payload?.resolve(e);
    }
}

function* serviceRecommendation(action) {
    const { payload } = action;
    try {
        const data = {candidate_id: payload?.candidate_id}
        const response = yield call(Api.fetchServiceRecommendation, data);
        if (response?.error) {
            return payload?.resolve(response.error)
        }

        const item = response?.data.data;
        const services = item.services;
        var service_list = Object.keys(services).map((key) => [Number(key), services[key]]);
        const value = { services: service_list, page:item.page}

        yield put(serviceRecommendationFetched({ ...item }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.error("Exception occured in service recommendation ", e);
        return payload?.resolve(e);
    }
}

function* uploadFile(action) {
    const { payload: { file1, resolve, reject } } = action;
    try {
        var fileData = new FormData();
        fileData.append('resume', file1);
        const result = yield call(Api.uploadFileUrlAPI, fileData);

        return resolve(result.data)
    }
    catch (error) {
        return reject(error)
    }
}

function* sendFeedbackData(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.sendFeedback, payload.feedData);

        if (response.error) return ;

        return ;
    }
    catch(e) {
        console.error("Exception occured in userIntent data", e);
        return ;
    }
}

export default function* WatchUserIntentPage() {
    yield takeLatest(fetchedUserIntentData.type, userIntentData);
    yield takeLatest(fetchFindRightJobsData.type, findJobsData);
    yield takeLatest(fetchUpskillYourselfData.type, upskillData);
    yield takeLatest(fetchServiceRecommendation.type, serviceRecommendation);
    yield takeLatest(uploadFileUrl.type, uploadFile);
    yield takeLatest(sendFeedback.type, sendFeedbackData);
}