import * as Actions from '../actions/actionTypes';

const initState = { }

export const DashboardMyOrdersReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_ORDERS_FETCHED : 
            return { 
                ...initState,
                ...action.item
            }
        case Actions.ORDER_CANCELLED : 
            return { 
                ...initState,
                ...action.item
            }
        default: 
            return state;
    }
}