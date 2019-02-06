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

const saveHomeData = (data) => {
    const url = 'users/';
    return BaseApiService.post(`http://127.0.0.1:8000/resume/api/v1/${url}`, data);
};

export const Api = {
    fetchHomeData,
    saveHomeData
};