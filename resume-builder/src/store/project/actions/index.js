import {FETCH_USER_PROJECT, UPDATE_USER_PROJECT} from './actionTypes'


export const fetchUserProject = () => {
    return {
        type: FETCH_USER_PROJECT
    }
}

export const updateUserProject = (payload) => {
    return {
        type: UPDATE_USER_PROJECT,
        payload
    }
}