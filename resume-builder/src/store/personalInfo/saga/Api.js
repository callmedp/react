import BaseApiService from '../../../services/BaseApiService'

const fetchPersonalInfo = (candidateId) => {

    const url = `users/${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            candidate_id: '',
            first_name: 'Amanpreet',
            last_name: 'Singh',
            email: 'amanpreet@gmail.com',
            number: '9958220358',
            image: '',
            date_of_birth: new Date('1995-12-05'),
            location: 'India',
            gender: 'Male',
        }
    }
};

const updatePersonalData = (data, candidateId) => {
    const url = `users/${candidateId}/`;
    //return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    return {
        data: {
            candidate_id: '',
            first_name: 'Sanam',
            last_name: 'Singh',
            email: 'sanam@gmail.com',
            number: '12399582201',
            image: '',
            date_of_birth: '10-10-1993',
            location: 'Delhi',
            gender: 'Male',
        }
    }
};


export const Api = {
    fetchPersonalInfo,
    updatePersonalData
}