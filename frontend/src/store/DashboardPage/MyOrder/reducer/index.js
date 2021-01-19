import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
    wal_total: 0,
    page: [],
    loyality_txns: []
}

export const DashboardMyOrdersReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_ORDERS_FETCHED : return { ...initState,...action.item}
        default: return state;
    }
}