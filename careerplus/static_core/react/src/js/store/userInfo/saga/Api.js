import BaseApiService from '../../../services/BaseApiService'

const saveUserData = (data) => {
    const url = 'users/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserExperience = (data) => {
    const url = 'user-experiences/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserEducation = (data) => {
    const url = 'user-educations/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserCertification = (data) => {
    const url = 'user-certifications/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserReference = (data) => {
    const url = 'user-references/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserProject = (data) => {
    const url = 'user-projects/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserSkill = (data) => {
    const url = 'skills/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const saveUserAchievement = (data) => {
    const url = 'user-achievements/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const updateUserData = (data, userId) => {
    const url = `users/${userId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data, {});
};

const fetchSkills = () => {
    const url = `skills/?page_size=10`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};


export const Api = {
    saveUserData,
    updateUserData,
    saveUserExperience,
    saveUserEducation,
    saveUserCertification,
    saveUserReference,
    saveUserProject,
    saveUserSkill,
    saveUserAchievement,
    fetchSkills
};