import React from 'react';
import { Link } from 'react-router-dom';
import './UIbanner.scss';

const UIBanner = (props) => {
    return (
       <div className="m-container mt-0 mb-0 m-ui-header-content">
            <h1 className="m-heading1"><strong>Career Guidance</strong> with personalized recommendations</h1>
       </div> 
    )
}

export default UIBanner;