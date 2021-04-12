import { createAction } from '@reduxjs/toolkit';

const fetchMainCourses = createAction('FETCH_MAIN_COURSES');
const mainCoursesFetched = createAction('MAIN_COURSES_FETCHED');

const fetchRecommendedCourses = createAction('FETCH_RECOMMENDED_COURSES');
const recommendedCoursesFetched = createAction('RECOMMENDED_COURSES_FETCHED');

const fetchProductReviews = createAction('FETCH_REVIEWS');
const ReviewsFetched = createAction('REVIEWS_FETCHED');
const submitReview = createAction('SUBMIT_REVIEW');

const sendEnquireNow = createAction('SEND_ENQUIRE_NOW');
const sendedEnquireNow = createAction('SENEDED_EQUIRE_NOW');

// add to cart action
const fetchAddToCartEnroll = createAction('FETCH_ADD_TO_CART_ENROLL');
const addToCartEnrollFetched = createAction('ADD_TO_CART_ENROLL_FETCHED');

// add to cart action redeem now
const fetchAddToCartRedeem = createAction('FETCH_ADD_TO_CART_REDEEM');
const addToCartRedeemFetched = createAction('ADD_TO_CART_REDEEM_FETCHED');

export {
    fetchMainCourses,
    mainCoursesFetched,
    fetchProductReviews,
    ReviewsFetched,
    submitReview,
    fetchRecommendedCourses,
    recommendedCoursesFetched,
    sendEnquireNow,
    sendedEnquireNow,
    fetchAddToCartEnroll,
    addToCartEnrollFetched,
    fetchAddToCartRedeem,
    addToCartRedeemFetched
}