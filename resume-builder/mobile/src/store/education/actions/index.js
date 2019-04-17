import {FETCH_USER_EDUCATION, UPDATE_USER_EDUCATION, BULK_UPDATE_USER_EDUCATION , DELETE_USER_EDUCATION} from './actionTypes'


export const fetchUserEducation = () => {
    return {
        type: FETCH_USER_EDUCATION
    }
};

export const updateUserEducation = (payload) => {
    return {
        type: UPDATE_USER_EDUCATION,
        payload
    }
};


export const deleteEducation = (educationId) => {
    return {
        type: DELETE_USER_EDUCATION,
        educationId
    }
}

export const bulkUpdateUserEducation = (payload) => {
    return {
        type: BULK_UPDATE_USER_EDUCATION ,
        payload
    }
}