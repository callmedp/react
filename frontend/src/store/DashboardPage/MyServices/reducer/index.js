import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
    page: {},
}

const resInitState = {
}

export const DashboardMyServicesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_SERVICES_FETCHED : return { ...initState, ...action.item}
        
        case Actions.CANDIDATE_OI_ACCEPT_REJECT_SUCCESS: {
            return {
                ...state, error: false
            };
        }

        case Actions.PAUSE_AND_RESUME_SERVICE_SUCCESS: {
            return {
                ...state, loading: false,
            }
        }
        
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