import {ADD_TO_CART , GET_PRODUCT_IDS} from './actionTypes'


export const addToCart = (payload) => ({
    type: ADD_TO_CART,
    payload
});

export const getProductIds = (payload) => ({
    type: GET_PRODUCT_IDS,
    payload
});
