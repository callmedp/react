import * as Actions from './actionTypes';

export const fetchRecommendedProducts = (payload) => ({
    type: Actions.FETCH_RECOMMENDED_PRODUCTS,
    payload
})