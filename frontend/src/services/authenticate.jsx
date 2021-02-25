import { useDispatch } from 'react-redux';
import { sessionAvailability, getCandidateInfo } from 'store/Header/actions/index'; 
import {  Toast } from "services/Toast";
import { useEffect, useState } from 'react';

const useAuthenticate = async () => {

    const dispatch = useDispatch();
    const [authenticate, setAuthenticate] = useState(false)

    const isSessionAvailable = async () => {
        localStorage.clear();
        try{
            const session = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));
            console.log("session hit", session)
            if(session['result'] === false){
                setAuthenticate(false);
            }
            else{
            const candidateId = session['candidate_id'];
            await new Promise((resolve, reject) => dispatch(getCandidateInfo({ candidateId, resolve, reject })));
            setAuthenticate(true);
            }
         
        }
        catch(e){
            console.log("error occured in fetching user session");
            Toast('error','Something went wrong. Cannot login')
            setAuthenticate(false)
           
        }
       
    }

    useEffect(() => {
        if(localStorage.getItem('isAuthenticated') === true){
            setAuthenticate(true);
        }
        else{
            isSessionAvailable();
        }
        
    },[])
    console.log("authenticate system", authenticate)
    return authenticate;
}

export default useAuthenticate;
