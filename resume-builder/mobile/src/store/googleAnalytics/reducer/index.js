import {LOCATION_ROUTE_CHANGE} from '../actions/actionTypes'

const initialState = {
    'locationPath':''
};


export const googleAnalyticsReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOCATION_ROUTE_CHANGE: {
            return {
                ...state,
                ...{
                    locationPath : action.payload
                }
            }
        }
        default: {
            return state;
        }
    }
};

