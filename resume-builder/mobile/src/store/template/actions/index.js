import {FETCH_TEMPLATE,UPDATE_MODAL_STATUS} from './actionTypes'


export const fetchTemplate = () => {
    return {
        type: FETCH_TEMPLATE
    }
}

export const updateModalStatus = (payload) => {
    return {
        type: UPDATE_MODAL_STATUS,
        payload
    }
}