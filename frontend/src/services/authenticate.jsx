import { useDispatch } from 'react-redux';
import { sessionAvailability } from 'store/Header/actions/index'; 



const useAuthenticate = () => {

    const dispatch = useDispatch();

  

    if(localStorage.getItem('isAuthenticated')){
        return true;
    }

    const isSessionAvailable = async () => {
        return await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));
    }
    
    if(isSessionAvailable()['result']){
        return true;
    }

    return false;

}

export default useAuthenticate;
