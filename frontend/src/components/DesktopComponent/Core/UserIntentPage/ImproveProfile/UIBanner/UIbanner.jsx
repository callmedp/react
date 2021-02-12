import React from 'react';
import { Link } from 'react-router-dom';
import './UIbanner.scss';

const UIBanner = (props) => {
    return (
       <header className="container-fluid pos-rel ui-bg">
            <div className="row">
                <div className="container ui-header-content mt-30">
                    <figure className="mr-20">
                        <i className="icon-ui1"></i>
                    </figure>
                    <h1 className="heading1">Career Guidance with personalized recommendations</h1>
                </div>
            </div>
       </header> 
    )
}

export default UIBanner;