import { 
    FETCHING_ALL_SERVICES
} from './actionTypes';


const fetchServices = (payload) => {
    
    return {
        type: FETCHING_ALL_SERVICES,
        payload
    } 
}


export {
    fetchServices
};