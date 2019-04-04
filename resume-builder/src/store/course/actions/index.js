import {FETCH_USER_COURSE, UPDATE_USER_COURSE} from './actionTypes'


export const fetchUserCourse = () => {
    return {
        type: FETCH_USER_COURSE
    }
}

export const updateUserCourse = (payload) => {
    return {
        type: UPDATE_USER_COURSE,
        payload
    }
}