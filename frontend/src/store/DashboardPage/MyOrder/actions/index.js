import { FETCH_MY_ORDERS  } from './actionTypes';

const fetchMyOrders = (payload) => {
    return {
        type : FETCH_MY_ORDERS,
        payload
    }
}

export {
    fetchMyOrders,
}