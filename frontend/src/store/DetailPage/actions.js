import { createAction } from '@reduxjs/toolkit';

const fetchOtherProviderCourses = createAction('FETCH_OTHER_PROVIDER_COURSES');
const OtherProviderCoursesFetched = createAction('OTHER_PROVIDER_COURSES_FETCHED');

export {
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched
}