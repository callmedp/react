import React  from 'react';
import './loader.scss'

export default function Loader() {
   

  
    return (
            <div className="">
                <div className="loader-page">
                    <span className="loader-img">
                        <img className="" src="media/images/loader.png" alt="loading"/>
                        <div className="please-wait">
                            Please wait...
                        </div>
                        
                    </span>
                </div>
            </div>
        )

}