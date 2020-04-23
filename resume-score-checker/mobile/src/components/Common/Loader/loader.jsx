import React , { useEffect } from 'react';
import './loader.scss'
import { imageUrl } from '../../../Utils/domains';

export default function Loader(){

    //used here to stop screen from scrolling while loader runs
    useEffect(() => {
        document.body.style.overflow = 'hidden';
        return ()=> document.body.style.overflow = 'unset';
     }, []);

    return(<div className="loader">
        <div className="loader__wrap">
        <img src={`${imageUrl}score-checker/images/mobile/loader.png`} width="64" height="64" alt=""/>
        <p>Please wait....</p>
        </div>
    </div>)
}