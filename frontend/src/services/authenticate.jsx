import React from 'react';
import { useDispatch } from 'react-redux';
import { sessionAvailability } from 'store/Header/actions/index'; 

const IsAuthenticated = async () => {

    const dispatch = useDispatch();

    if(localStorage.getItem('isAuthenticated')){
        return true;
    }
    const isSessionAvailable = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));
    if(isSessionAvailable['result']){
        return true;
    }

    return false;

}

export default IsAuthenticated;