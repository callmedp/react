import { createAction } from '@reduxjs/toolkit';

const fetchMainCourses = createAction('FETCH_MAIN_COURSES');
const mainCoursesFetched = createAction('MAIN_COURSES_FETCHED');

const fetchOtherProviderCourses = createAction('FETCH_OTHER_PROVIDER_COURSES');
const OtherProviderCoursesFetched = createAction('OTHER_PROVIDER_COURSES_FETCHED');

const fetchCourseReview = createAction("FETCH_COURSE_REVIEW");
const CourseReviewFetched = createAction("COURSE_REVIEW_FETCHED")

export {
    fetchMainCourses,
    mainCoursesFetched,
    fetchOtherProviderCourses,
    OtherProviderCoursesFetched,
    fetchCourseReview,
    CourseReviewFetched
}