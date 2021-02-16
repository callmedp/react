import { createAction } from '@reduxjs/toolkit';

const sendUserIntentData = createAction('SEND_USER_INTENT_DATA');
const fetchedUserIntentData = createAction('FETCHED_USER_INTENT_DATA');


export {
    sendUserIntentData,
    fetchedUserIntentData
}