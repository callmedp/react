import {FETCH_USER_SKILL, UPDATE_USER_SKILL} from './actionTypes'


export const fetchUserSkill = () => {
    return {
        type: FETCH_USER_SKILL
    }
}

export const updateUserSkill = (payload) => {
    return {
        type: UPDATE_USER_SKILL,
        payload

    }
}