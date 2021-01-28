import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
    page: {},
}

const resInitState = {
}

export const DashboardMyServicesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_SERVICES_FETCHED : return { ...initState,...action.item}

        default: return state;
    }
}

export const DashboardMyServicesResumeReducer = (state=resInitState, action) => {
    switch(action.type){
        case Actions.PENDING_RESUME_FETCHED: {
            return { ...state, ...action.data };
        }

        default: return state;
    }
}