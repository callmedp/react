import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
    pending_resume_items: [],
    page: {},
}

export const DashboardMyServicesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_SERVICES_FETCHED : return { ...initState,...action.item}

        case Actions.PENDING_RESUMES_FETCHED: {
            return {
                ...state, ...action.item
            }
        }

        case Actions.CANDIDATE_OI_ACCEPT_REJECT_SUCCESS: {
            return {
                ...state, error: false
            };
        }

        default: return state;
    }
}