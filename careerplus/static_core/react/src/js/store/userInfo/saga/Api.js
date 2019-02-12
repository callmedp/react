import BaseApiService from '../../../services/BaseApiService'

const fetchHomeData = () => {
    const url = '/home';
    // return BaseApiService.get(url);
    return {
        "location": "Bangalore",
        "pinCode": 110020,
        "state": "Karnataka"
    }
};

const saveUserData = (data) => {
    const url = 'users/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserExperience = (data) => {
    const url = 'user-experiences/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserEducation = (data) => {
    const url = 'user-educations/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserCertification = (data) => {
    const url = 'user-certifications/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserReference = (data) => {
    const url = 'user-references/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserProject = (data) => {
    const url = 'user-projects/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserSkill = (data) => {
    const url = 'skills/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const saveUserAchievement = (data) => {
    const url = 'user-achievements/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const updateUserData = (data, userId) => {
    const url = `users/${userId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

const fetchSkills = () => {
    const url = `skills/?page_size=10`;
    return BaseApiService.get(`http://127.0.0.1:8000/resume/api/v1/${url}`);
};


export const Api = {
    fetchHomeData,
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