import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
}

export const ReviewsReducer = (state = initState, action) => {
    console.log(action)
    switch(action.type) {
        case Actions.REVIEWS_FETCHED: {
            return { ...state, ...action.reviews };
        }

        case Actions.REVIEW_SUBMIT: {
            return { ...state, ...action.new_review };
        }

        default: return state;
    }
}
