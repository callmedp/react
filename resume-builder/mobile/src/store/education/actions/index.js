import {FETCH_USER_EDUCATION, UPDATE_USER_EDUCATION} from './actionTypes'


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
