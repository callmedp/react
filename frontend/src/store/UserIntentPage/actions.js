import { createAction } from '@reduxjs/toolkit';

const sendUserIntentData = createAction('SEND_USER_INTENT_DATA');
const fetchedUserIntentData = createAction('FETCHED_USER_INTENT_DATA');

const fetchCareerChangeData = createAction('FETCH_CAREER_CHANGE_DATA');
const careerChangeDataFetched = createAction('CAREER_CHANGE_DATA_FETCHED');

// find jobs
const fetchFindRightJobsData = createAction('FETCH_FIND_RIGHT_JOBS_DATA');
const findRightJobsDataFetched = createAction('FIND_RIGHT_JOBS_DATA_FETCHED');

// upskill yourself
const fetchUpskillYourselfData = createAction('FETCH_UPSKILL_YOURSELF_DATA');
const upskillYourselfDataFetched = createAction('UPSKILL_YOURSELF_DATA_FETCHED');

const sendFeedback = createAction('SEND_FEEDBACK');

export {
    sendUserIntentData,
    fetchedUserIntentData,
    fetchCareerChangeData,
    careerChangeDataFetched,
    fetchFindRightJobsData,
    findRightJobsDataFetched,
    fetchUpskillYourselfData,
    upskillYourselfDataFetched,
    sendFeedback,
}