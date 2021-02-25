import { createAction } from '@reduxjs/toolkit';

const sendUserIntentData = createAction('SEND_USER_INTENT_DATA');
const fetchedUserIntentData = createAction('FETCHED_USER_INTENT_DATA');

// find jobs
const fetchFindRightJobsData = createAction('FETCH_FIND_RIGHT_JOBS_DATA');
const findRightJobsDataFetched = createAction('FIND_RIGHT_JOBS_DATA_FETCHED');

// upskill yourself
const fetchUpskillYourselfData = createAction('FETCH_UPSKILL_YOURSELF_DATA');
const upskillYourselfDataFetched = createAction('UPSKILL_YOURSELF_DATA_FETCHED');

const fetchServiceRecommendation = createAction('FETCH_SERVICE_RECOMMENDATION');
const serviceRecommendationFetched = createAction('SERVICE_RECOMMENDATION_FETCHED');

const uploadFileUrl = createAction('UPLOAD_FILE_URL');

// send feedback
const sendFeedback = createAction('SEND_FEEDBACK');

export {
    sendUserIntentData,
    fetchedUserIntentData,
    fetchFindRightJobsData,
    findRightJobsDataFetched,
    fetchUpskillYourselfData,
    upskillYourselfDataFetched,
    serviceRecommendationFetched,
    fetchServiceRecommendation,
    uploadFileUrl,
    sendFeedback
}