import React from 'react';
import './loader.scss'
import { imageUrl } from '../../../Utils/domains';

const Loader = ()=>
    (<div className="loader">
        <div className="loader__wrap">
        <img src={`${imageUrl}score-checker/images/mobile/loader.png" width="64" height="64"`} alt=""/>
        <p>Please wait....</p>
        </div>
    </div>)

export default Loader;