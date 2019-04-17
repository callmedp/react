import {
    FETCH_USER_EXPERIENCE,
    UPDATE_USER_EXPERIENCE,
    DELETE_USER_EXPERIENCE,
    BULK_UPDATE_USER_EXPERIENCE
} from './actionTypes'


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
};


export const deleteExperience = (experienceId) => {
    return {
        type: DELETE_USER_EXPERIENCE,
        experienceId
    }
}

export const bulkUpdateUserExperience = (payload) => {
    return {
        type: BULK_UPDATE_USER_EXPERIENCE,
        payload
    }
};