import {FETCH_USER_COURSE, UPDATE_USER_COURSE, DELETE_USER_COURSE, HANDLE_COURSE_SWAP} from './actionTypes'


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


export const deleteCourse = (courseId) => {
    return {
        type: DELETE_USER_COURSE,
        courseId
    }
}

export const handleCourseSwap = (payload) => {
    return {
        type: HANDLE_COURSE_SWAP,
        payload
    }
};