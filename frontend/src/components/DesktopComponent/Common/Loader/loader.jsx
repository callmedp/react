import React, {useEffect}  from 'react';
import './loader.scss';
import {imageUrl} from 'utils/domains'

export default function Loader() {
   
   

  
    return (
                <div className="loader-page">
                    <span className="loader-img">
                        <img className="" src={`${imageUrl}desktop/loader.png`} alt="loading"/>
                        <div className="please-wait">
                            Please wait...
                        </div>
                        
                    </span>
                </div>
        )

}