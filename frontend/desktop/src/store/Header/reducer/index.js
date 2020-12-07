import * as Actions from '../actions/actionTypes';

const initState = {
    count : 0,
    navTags : [],
    navOffer : [],
}

export const HeaderReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.CART_COUNT_FETCHED : return {...state, ...action.item}
        case Actions.NAVIGATION_OFFERS_AND_SPECIAL_TAGS_FETCHED : return {...state, ...action.item}
        default: return state;
    }
}