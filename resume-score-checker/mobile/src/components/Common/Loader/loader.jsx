import React from 'react';
import './loader.scss'

const Loader = ()=>
    (<div className="loader">
        <div className="loader__wrap">
        <img src="media/images/loader.png" width="64" height="64" alt=""/>
        <p>Please wait....</p>
        </div>
    </div>)

export default Loader;