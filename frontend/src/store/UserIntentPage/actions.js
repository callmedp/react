import { createAction } from '@reduxjs/toolkit';

// find jobs
const fetchFindRightJobsData = createAction('FETCH_FIND_RIGHT_JOBS_DATA');
const findRightJobsDataFetched = createAction('FIND_RIGHT_JOBS_DATA_FETCHED');

// upskill yourself
const fetchUpskillYourselfData = createAction('FETCH_UPSKILL_YOURSELF_DATA');
const upskillYourselfDataFetched = createAction('UPSKILL_YOURSELF_DATA_FETCHED');
const upskillAndJobsCleanup = createAction('UPSKILL_AND_JOBS_CLEANUP');

const fetchServiceRecommendation = createAction('FETCH_SERVICE_RECOMMENDATION');
const serviceRecommendationFetched = createAction('SERVICE_RECOMMENDATION_FETCHED');

const uploadFileUrl = createAction('UPLOAD_FILE_URL');

// send feedback
const sendFeedback = createAction('SEND_FEEDBACK');

export {
    fetchFindRightJobsData,
    findRightJobsDataFetched,
    fetchUpskillYourselfData,
    upskillYourselfDataFetched,
    serviceRecommendationFetched,
    fetchServiceRecommendation,
    uploadFileUrl,
    sendFeedback,
    upskillAndJobsCleanup
}