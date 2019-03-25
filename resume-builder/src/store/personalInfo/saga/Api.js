import BaseApiService from '../../../services/BaseApiService'

const fetchPersonalInfo = () => {
    const url = 'users/';
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`);

}


export const Api = {
    fetchPersonalInfo
}