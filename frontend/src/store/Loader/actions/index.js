import * as Actions from './actionTypes';

export const startSkillPageLoader = () => {
    return {
        type: Actions.START_SKILL_PAGE_LOADER,
        payload: { skillLoader: true } 
    }
}

export const stopSkillPageLoader = () => {
    return {
        type: Actions.STOP_SKILL_PAGE_LOADER,
        payload: { skillLoader: false }
    }
}