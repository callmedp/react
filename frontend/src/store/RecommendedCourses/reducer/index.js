import * as Actions from '../actions/actionTypes';

const initState = {
    r_courses : [],
    r_assesments : []
}

export const RecommendationReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.RECOMMENDED_PRODUCTS_FETCHED : return {...state, ...action.item}
        default: return state;
    }
}