import { 
    FETCH_RECENTLY_ADDED_SERVICES
} from './actionTypes';


const fetchServices = (payload) => {
    
    return {
        type: FETCH_RECENTLY_ADDED_SERVICES,
        payload
    } 
}


export {
    fetchServices
}