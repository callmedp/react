import {
    FETCH_HOME_DATA, SAVE_USER_DETAILS, UPDATE_USER_DETAILS, SAVE_USER_EXPERIENCES,
    SAVE_USER_EDUCATION, SAVE_USER_CERTIFICATION, SAVE_USER_REFERENCE, SAVE_USER_PROJECT,
    SAVE_USER_ACHIEVEMENT, FETCH_SKILL_LIST, FETCH_DEFAULT_SKILL_LIST, ADD_PROJECT,
    GET_PROJECT_DETAIL, ADD_EXPERIENCE, ADD_EDUCATION, ADD_CERTIFICATION, ADD_ACHIEVEMENT,
    ADD_REFERENCE, ADD_SKILL, SAVE_USER_SKILL, ADD_TO_CART, SHOW_RESUME_PREVIEW
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

export const addExperience = (data) => ({
    type: ADD_EXPERIENCE,
    data
});


export const saveUserEducation = (payload) => ({
    type: SAVE_USER_EDUCATION,
    payload
});


export const addEducation = (data) => ({
    type: ADD_EDUCATION,
    data
});


export const saveUserCertification = (payload) => ({
    type: SAVE_USER_CERTIFICATION,
    payload
});


export const addCertification = (data) => ({
    type: ADD_CERTIFICATION,
    data
});

export const saveUserReference = (payload) => ({
    type: SAVE_USER_REFERENCE,
    payload
});


export const addReference = (data) => ({
    type: ADD_REFERENCE,
    data
});

export const saveUserProject = (payload) => ({
    type: SAVE_USER_PROJECT,
    payload
});

export const addProject = (data) => ({
    type: ADD_PROJECT,
    data
});

export const saveUserSkill = (payload) => ({
    type: SAVE_USER_SKILL,
    payload
});


export const addSkill = (data) => ({
    type: ADD_SKILL,
    data
});

export const getProjectDetail = (data) => ({
    type: GET_PROJECT_DETAIL,
    data

})


export const saveUserAchievement = (payload) => ({
    type: SAVE_USER_ACHIEVEMENT,
    payload
});


export const addAchievement = (data) => ({
    type: ADD_ACHIEVEMENT,
    data
});

export const fetchDefaultSkillList = (inputValue) => ({
    type: FETCH_DEFAULT_SKILL_LIST,
    inputValue
});

export const addToCart = () => ({
    type: ADD_TO_CART
});

export const showResumePreview = (payload) => ({
    type: SHOW_RESUME_PREVIEW,
    payload
})

