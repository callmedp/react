import { FETCH_ORDER_DETAILS  } from './actionTypes';

const fetchOrderDetails = (payload) => {
    return {
        type : FETCH_ORDER_DETAILS,
        payload
    }
}

export {
    fetchOrderDetails,
}