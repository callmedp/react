import React from 'react';
import { Link } from 'react-router-dom';
import './UIbanner.scss';

const UIBanner1 = (props) => {
    return (
       <header className="container-fluid pos-rel ui-bg">
            <div className="row">
                <div className="container ui-header-content mt-30">
                    <figure className="mr-20">
                        <i className="icon-ui2"></i>
                    </figure>
                    <h1 className="heading1">Find the right job</h1>
                    <Link className="goal btn btn-outline-white" to={"#"}><i className="icon-back-goal mr-10"></i>Back to goal</Link>
                </div>
            </div>
       </header> 
    )
}

export default UIBanner1;