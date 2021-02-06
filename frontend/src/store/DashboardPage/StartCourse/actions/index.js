import { GET_VENDOR_URL } from './actionTypes';

const getVendorUrl = (payload) =>{
    return{
        type : GET_VENDOR_URL,
        payload
    }
}

export {
    getVendorUrl
}