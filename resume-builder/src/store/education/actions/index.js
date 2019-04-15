import {FETCH_USER_EDUCATION, UPDATE_USER_EDUCATION, HANDLE_EDUCATION_SWAP, REMOVE_EDUCATION} from './actionTypes'


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


export const handleEducationSwap = (educationId) => {
    return {
        type: HANDLE_EDUCATION_SWAP,
        educationId
    }
}

export const deleteEducation = (payload) => {
    return {
        type: REMOVE_EDUCATION,
        payload
    }
}