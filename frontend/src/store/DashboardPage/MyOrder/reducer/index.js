import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
    page: {},
    error: false,
    message: ""
}

export const DashboardMyOrdersReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_ORDERS_FETCHED : return { ...initState,...action.item}
        default: return state;
    }
}