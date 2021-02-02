import { createAction } from '@reduxjs/toolkit';

const fetchMostViewedCourses = createAction('FETCH_MOST_VIEWED_PRODUCTS');
const mostViewedCoursesFetched = createAction('MOST_VIEWED_PRODUCTS_FETCHED');

const fetchInDemandProducts = createAction('FETCH_IN_DEMAND_PRODUCTS');
const inDemandProductsFetched = createAction('IN_DEMAND_PRODUCTS_FETCHED');

const fetchJobAssistanceAndBlogs = createAction('FETCH_JOB_ASSISTANCE_AND_BLOGS');
const jobAssistanceAndBlogsFetched = createAction('JOB_ASSISTANCE_AND_BLOGS_FETCHED');

export {
    fetchMostViewedCourses,
    fetchInDemandProducts,
    fetchJobAssistanceAndBlogs,
    mostViewedCoursesFetched,
    inDemandProductsFetched,
    jobAssistanceAndBlogsFetched,
}