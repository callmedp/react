import * as Actions from '../actions/actionTypes';

const initState = {
    skillLoader : false
}

export const LoaderReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.START_SKILL_PAGE_LOADER : return {...state, ...action.payload}
        case Actions.STOP_SKILL_PAGE_LOADER : return {...state, ...action.payload}
        default: return state;
    }
}