import {FETCH_USER_SKILL, UPDATE_USER_SKILL, BULK_SAVE_USER_SKILL, DELETE_USER_SKILL} from './actionTypes'


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

export const bulkSaveUserSkill = (payload) => {
    return {
        type: BULK_SAVE_USER_SKILL,
        payload
    }
}

export const deleteSkill = (skillId) => {
    return {
        type: DELETE_USER_SKILL,
        skillId
    }
}

