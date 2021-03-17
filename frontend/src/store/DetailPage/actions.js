import { createAction } from '@reduxjs/toolkit';

const fetchOtherProviderCourses = createAction('FETCH_OTHER_PROVIDER_COURSES');
const OtherProviderCoursesFetched = createAction('OTHER_PROVIDER_COURSES_FETCHED');

const fetchRecommendedCourses = createAction('FETCH_RECOMMENDED_COURSES');
const recommendedCoursesFetched = createAction('RECOMMENDED_COURSES_FETCHED');

const fetchReviews = createAction('FETCH_REVIEWS');
const ReviewsFetched = createAction('REVIEWS_FETCHED');
const submitReview = createAction('SUBMIT_REVIEW');

export {
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    fetchReviews,
    ReviewsFetched,
    submitReview,
    fetchRecommendedCourses,
    recommendedCoursesFetched
}