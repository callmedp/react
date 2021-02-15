import * as Actions from './actionTypes';

const fetchReviews = (payload) => {
    return {
        type : Actions.FETCH_REVIEWS,
        payload
    }
}

const submitReview = (payload) => {
    return {
        type : Actions.REVIEW_SUBMIT,
        payload
    }
}

export {
    fetchReviews,
    submitReview
}