import {FETCH_USER_SKILL, UPDATE_USER_SKILL, HANDLE_SKILL_SWAP, DELETE_USER_SKILL} from './actionTypes'


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


export const deleteSkill = (skillId) => {
    return {
        type: DELETE_USER_SKILL,
        skillId
    }
}

export const handleSkillSwap = (payload) => {
    return {
        type: HANDLE_SKILL_SWAP,
        payload
    }
}