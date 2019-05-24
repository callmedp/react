import {UPDATE_MAIN_PAGE_LOADER,UPDATE_DATA_LOADER,FETCH_LOADER_STATUS,CHANGE_FORM_NAME} from './actionTypes'


export const updateMainLoader = (payload) => {
    return {
        type: UPDATE_MAIN_PAGE_LOADER,
        payload
    }
}

export const updateDataLoader = (payload) => {
    return {
        type: UPDATE_DATA_LOADER,
        payload
    }
}

export const fetchLoaderStatus = () => {
    return {
        type: FETCH_LOADER_STATUS,
    }
}

export const changeFormName = (payload) => {
    return {
        type: CHANGE_FORM_NAME,
        payload
    }
}