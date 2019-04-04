import {FETCH_USER_EXPERIENCE, UPDATE_USER_EXPERIENCE} from './actionTypes'


export const fetchUserExperience = () => {
    return {
        type: FETCH_USER_EXPERIENCE
    }
}


export const updateUserExperience = (payload) => {
    return {
        type: UPDATE_USER_EXPERIENCE,
        payload
    }
}

