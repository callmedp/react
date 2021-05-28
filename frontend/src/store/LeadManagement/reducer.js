import { leadManagementFetched } from './actions';

const leadManagementState = {}

export const leadManagementReducer = (state = leadManagementState, action) => {
    switch (action.type) {
        case leadManagementFetched.type: return { ...action.payload } 
        default: return state;
    }
}