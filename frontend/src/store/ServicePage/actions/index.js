import { 
    FETCH_MY_SERVICE
} from './actionTypes';


const fetchServices = (payload) => {
    
    return {
        type: FETCH_MY_SERVICE,
        payload
    } 
}


export {
    fetchServices
}