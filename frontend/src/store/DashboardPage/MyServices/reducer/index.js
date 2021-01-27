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
        default: return state;
    }
}