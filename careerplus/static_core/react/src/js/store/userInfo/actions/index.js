import {
    FETCH_HOME_DATA, SAVE_USER_DETAILS, UPDATE_USER_DETAILS, SAVE_USER_EXPERIENCES,
    SAVE_USER_EDUCATION, SAVE_USER_CERTIFICATION, SAVE_USER_REFERENCE, SAVE_USER_PROJECT,
    SAVE_USER_ACHIEVEMENT, FETCH_SKILL_LIST, FETCH_DEFAULT_SKILL_LIST
} from "./actionTypes";

export const fetchHomeData = () => ({
    type: FETCH_HOME_DATA
});

export const fetchSkillList = (payload) => ({
    type: FETCH_SKILL_LIST,
    payload
});

export const saveUserDetails = (payload) => ({
    type: SAVE_USER_DETAILS,
    payload
});

export const updateUserDetails = (payload) => ({
    type: UPDATE_USER_DETAILS,
    payload
});

export const saveUserExperience = (payload) => ({
    type: SAVE_USER_EXPERIENCES,
    payload
});

export const saveUserEducation = (payload) => ({
    type: SAVE_USER_EDUCATION,
    payload
});

export const saveUserCertification = (payload) => ({
    type: SAVE_USER_CERTIFICATION,
    payload
});

export const saveUserReference = (payload) => ({
    type: SAVE_USER_REFERENCE,
    payload
});

export const saveUserProject = (payload) => ({
    type: SAVE_USER_PROJECT,
    payload
});

export const saveUserAchievement = (payload) => ({
    type: SAVE_USER_ACHIEVEMENT,
    payload
});

export const fetchDefaultSkillList = (inputValue) => ({
    type: FETCH_DEFAULT_SKILL_LIST,
    inputValue
});


