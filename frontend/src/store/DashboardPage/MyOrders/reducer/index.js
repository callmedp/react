import * as Actions from '../actions/actionTypes';

const initState = {
    orderList : []
}

export const DashboardOrdersReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.ORDER_DETAILS_FETCHED : return { ...initState,...action.item}
        
        default: return state;
    }
}