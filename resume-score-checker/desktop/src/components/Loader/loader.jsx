import React  from 'react';
import './loader.scss';
import {imageUrl} from '../../utils/domains'
export default function Loader() {
   
    useEffect(()=>{
        document.body.style.overflow = 'hidden';
        return () => document.body.style.overflow = 'unset';
    },[])

  
    return (
            <div className="">
                <div className="loader-page">
                    <span className="loader-img">
                        <img className="" src={`${imageUrl}score-checker/images/loader.png`} alt="loading"/>
                        <div className="please-wait">
                            Please wait...
                        </div>
                        
                    </span>
                </div>
            </div>
        )

}