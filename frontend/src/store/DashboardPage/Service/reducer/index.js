import * as Actions from '../actions/actionTypes';

const recentServicesState = {
    data: { },
    error: false,
    message: ""
}

export const RecentlyServicesReducer = (state = recentServicesState, action) => {
    console.log(action);
    switch(action.type) {
        case Actions.FETCHING_ALL_SERVICES : return {...recentServicesState, ...action.item}
        default : return state;
    }
}