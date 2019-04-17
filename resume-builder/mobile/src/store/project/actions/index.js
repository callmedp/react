import {FETCH_USER_PROJECT, UPDATE_USER_PROJECT, DELETE_USER_PROJECT, BULK_UPDATE_USER_PROJECT} from './actionTypes'


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

export const deleteProject = (projectId) => {
    return {
        type: DELETE_USER_PROJECT,
        projectId
    }
}

export const bulkUpdateUserProject = (payload) => {
    return {
        type: BULK_UPDATE_USER_PROJECT,
        payload
    }
}