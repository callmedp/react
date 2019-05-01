import {UPDATE_MAIN_PAGE_LOADER,UPDATE_DATA_LOADER} from './actionTypes'


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