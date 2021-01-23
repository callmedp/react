import { FETCH_MY_ORDERS, CANCEL_ORDER  } from './actionTypes';

const fetchMyOrders = (payload) => {
    return {
        type : FETCH_MY_ORDERS,
        payload
    }
}

const cancelOrder = payload => {
    return {
        type : CANCEL_ORDER,
        payload
    }
}

export {
    fetchMyOrders,
    cancelOrder
}