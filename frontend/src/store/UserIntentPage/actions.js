import { createAction } from '@reduxjs/toolkit';

const sendUserIntentData = createAction('SEND_USER_INTENT_DATA');
const fetchedUserIntentData = createAction('FETCHED_USER_INTENT_DATA');

const fetchCareerChangeData = createAction('FETCH_CAREER_CHANGE_DATA');
const careerChangeDataFetched = createAction('CAREER_CHANGE_DATA_FETCHED');


export {
    sendUserIntentData,
    fetchedUserIntentData,
    fetchCareerChangeData,
    careerChangeDataFetched
}