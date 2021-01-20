import { FETCH_MY_WALLET  } from './actionTypes';

const fetchMyWallet = (payload) => {
    return {
        type : FETCH_MY_WALLET,
        payload
    }
}

export {
    fetchMyWallet,
}