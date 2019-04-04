import BaseApiService from '../../../services/BaseApiService'

const fetchUserExperience = (candidateId) => {

    const url = `candidate/${candidateId}/experiences/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         job_profile: 'Software Engineer',
    //         company_name: 'HT Media Pvt Ltd',
    //         start_date: '12-12-1995',
    //         end_date: '22-12-2020',
    //         is_working: true,
    //         job_location: 'Gurugram',
    //         work_description: 'It is a dynamic task to do where you need to integrate it with data.',
    //     }
    // }
};

const updateUserExperience = (data, candidateId, experienceId = '') => {

    const url = `candidate/${candidateId}/experiences/${experienceId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         job_profile: 'Software Engineer',
    //         company_name: 'HT Media Pvt Ltd',
    //         start_date: '12-12-1995',
    //         end_date: '22-12-2020',
    //         is_working: true,
    //         job_location: 'Gurugram',
    //         work_description: 'It is a dynamic task to do where you need to integrate it with data.',
    //     }
    // }
};


const createUserExperience = (data, candidateId, experienceId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/experiences/`;

    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);

};


export const Api = {
    fetchUserExperience,
    updateUserExperience,
    createUserExperience
}