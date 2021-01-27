import * as Actions from '../actions/actionTypes';

const initState = {
    // reviews: [],
}

export const ReviewsReducer = (state = initState, action) => {
    switch(action.type){
        case Actions.REVIEWS_FETCHED: {
            return { ...state, ...action.reviews };
        }

        default: return state;
    }
}
