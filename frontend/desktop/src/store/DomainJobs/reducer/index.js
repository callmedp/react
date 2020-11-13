import { DOMAIN_JOBS_FETCHED } from "../actions/actionTypes";
import * as Actions from '../actions/actionTypes';

const initState = {

}

export const DomainJobsReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.DOMAIN_JOBS_FETCHED : return {...state, action}
        
        default: return state;
    }
}