import * as Actions from '../actions/actionTypes';

const initState = {
    navTags : [],
    navOffer : [],
}

export const NavigationReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.NAVIGATION_OFFERS_AND_SPECIAL_TAGS_FETCHED : return {...state, ...action.item}

        default: return state;
    }
}