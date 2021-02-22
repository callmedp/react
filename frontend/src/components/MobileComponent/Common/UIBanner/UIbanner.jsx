import React from 'react';
import { Link } from 'react-router-dom';
import './UIbanner.scss';

const UIBanner = (props) => {
    const { heading } = props;

    return (
        <div className="m-container mt-0 mb-0 m-ui-header-content">
            <h1 className="m-heading1" dangerouslySetInnerHTML={{__html: heading}}></h1>
        </div> 
    )
}

export default UIBanner;