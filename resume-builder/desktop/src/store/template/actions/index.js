import {FETCH_TEMPLATE} from './actionTypes'


export const fetchTemplate = (payload) => {
    return {
        type: FETCH_TEMPLATE,
        payload
    }
}