import BaseApiService from '../../../services/BaseApiService'
import moment from 'moment'

const fetchPersonalInfo = (candidateId) => {

    const url = `candidates/${candidateId}/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         first_name: 'Amanpreet',
    //         last_name: 'Singh',
    //         email: 'amanpreet@gmail.com',
    //         number: '9958220358',
    //         image: '',
    //         date_of_birth: moment('1995-12-05').format('YYYY-MM-DD'),
    //         location: 'India',
    //         gender: {"label":"Male", "value":"M"},
    //     }
    // }
};

const updatePersonalData = (data, candidateId) => {
    const url = `candidates/${candidateId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         candidate_id: '',
    //         first_name: 'Sanam',
    //         last_name: 'Singh',
    //         email: 'sanam@gmail.com',
    //         number: '12399582201',
    //         image: '',
    //         date_of_birth: '10-10-1993',
    //         location: 'Delhi',
    //         gender: 'Male',
    //     }
    // }
};

const fetchImageUrl = (data) => {
    const url = `media-upload/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/${url}`, data,
        {}, false, true);
};


export const Api = {
    fetchPersonalInfo,
    updatePersonalData,
    fetchImageUrl
}