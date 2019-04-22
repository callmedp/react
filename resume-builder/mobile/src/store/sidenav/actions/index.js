import {FETCH_SIDENAV_STATUS, UPDATE_SIDENAV_STATUS, FETCH_LIST_LINK ,UPDATE_LIST_LINK,UPDATE_CURRENT_LINK_POS} from './actionTypes'


export const fetchSideNavStatus = () => {
    return {
        type: FETCH_SIDENAV_STATUS
    }
}

export const updateSidenavStatus = (payload) => {
    return {
        type: UPDATE_SIDENAV_STATUS,
        payload
    }
}

export const fetchListOfLink = () => {
    return {
        type: FETCH_LIST_LINK
    }
}

export const updateListOfLink = (payload) => {
    return {
        type: UPDATE_LIST_LINK,
        payload
    }
}

export const updateCurrentLinkPos = (payload) => {
    return {
        type: UPDATE_CURRENT_LINK_POS,
        payload
    }
}