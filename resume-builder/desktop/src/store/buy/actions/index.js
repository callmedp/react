import {ADD_TO_CART , GET_PRODUCT_IDS, REQUEST_FREE_RESUME, POLLING_FREE_RESUME, DOWNLOAD_FREE_RESUME} from './actionTypes'


export const addToCart = (payload) => ({
    type: ADD_TO_CART,
    payload
});

export const getProductIds = (payload) => ({
    type: GET_PRODUCT_IDS,
    payload
});

export const requestFreeResume = (payload) => ({
    type: REQUEST_FREE_RESUME,
    payload
});


