import * as Actions from '../actions/actionTypes';

export const FetchUserInfoReducer = (state={}, action) => {
    switch(action.type){
        case Actions.FETCH_USER : return {...state, ...action.item}
        default: return state;
    }
}
