import { createAction } from '@reduxjs/toolkit';

const fetchMainCourses = createAction('FETCH_MAIN_COURSES');
const mainCoursesFetched = createAction('MAIN_COURSES_FETCHED');

const fetchOtherProviderCourses = createAction('FETCH_OTHER_PROVIDER_COURSES');
const OtherProviderCoursesFetched = createAction('OTHER_PROVIDER_COURSES_FETCHED');

const fetchReviews = createAction('FETCH_REVIEWS');
const ReviewsFetched = createAction('REVIEWS_FETCHED');
const submitReview = createAction('SUBMIT_REVIEW');

export {
    fetchMainCourses,
    mainCoursesFetched,
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    fetchReviews,
    ReviewsFetched,
    submitReview,
}