import BaseApiService from '../../../services/BaseApiService'

const fetchUserExperience = (candidateId) => {

    const url = `user-experience/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
             job_profile: 'Software Engineer',
    company_name: 'HT Media Pvt Ltd',
    start_date: '12-12-1995',
    end_date: '22-12-2020',
    is_working: true,
    job_location: '',
    work_description: 'It is a dynamic task to do where you need to integrate it with data.',
        }
    }
};


export const Api = {
    fetchUserExperience
}