import * as Actions from '../actions/actionTypes';

const initState = {
    data: {
        item_count: 0,
        order: {},
        orderitems: {},
        product_id: 0,
        product_type_flow: 0
    },
    error: false,
    message: ""
}

export const DashboardMyOrdersReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_ORDERS_FETCHED : return { ...initState,...action.item}
        default: return state;
    }
}