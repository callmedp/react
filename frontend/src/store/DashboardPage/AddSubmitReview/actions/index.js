import * as Actions from './actionTypes';

const fetchReviews = (payload) => {
    return {
        type : Actions.FETCH_REVIEWS,
        payload
    }
}

export {
    fetchReviews,
}