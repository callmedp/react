import * as Actions from '../actions/actionTypes';

const recentServicesState = {
    recentServicesList: []
}

export const RecentlyServicesReducer = (state = recentServicesState, action) => {
    switch(action.type) {
        case Actions.RECENTLY_ADDED_SERVICES_FETCHED : return {...recentServicesState, ...action.item}
        default : return state;
    }
}