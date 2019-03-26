import BaseApiService from '../../../services/BaseApiService'

const fetchPersonalInfo = () => {
    const url = 'user-profile/chopra_gaurav18@yahoo.com/';
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

export const Api = {
    fetchPersonalInfo
}