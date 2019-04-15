import {FETCH_USER_PROJECT, UPDATE_USER_PROJECT, DELETE_USER_PROJECT, HANDLE_PROJECT_SWAP} from './actionTypes'


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

export const handleProjectSwap = (payload) => {
    return {
        type: HANDLE_PROJECT_SWAP,
        payload
    }
}