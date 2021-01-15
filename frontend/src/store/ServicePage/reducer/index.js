import * as Actions from '../actions/actionTypes';

const recentServicesState = {
    recentServicesList: []
}

export const RecentlyServicesReducer = (state = recentServicesState, action) => {
    switch(action.type) {
        case Actions.FETCH_MY_SERVICE : return {...recentServicesState, ...action.item}
        default : return state;
    }
}