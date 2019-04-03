import {ADD_TO_CART , GET_PRODUCT_IDS} from './actionTypes'


export const addToCart = () => ({
    type: ADD_TO_CART
});

export const getProductIds = (payload) => ({
    type: GET_PRODUCT_IDS,
    payload
});