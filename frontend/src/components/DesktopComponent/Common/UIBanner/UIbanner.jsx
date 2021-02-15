import React from 'react';
import { Link } from 'react-router-dom';
import './UIbanner.scss';

const UIBanner = (props) => {

    const { title, back, icon } = props;

    return (
       <header className="container-fluid pos-rel ui-bg">
            <div className="row">
                <div className="container ui-header-content mt-30">
                    <figure className="mr-20">
                        <i className={icon}></i>
                    </figure>
                    <h1 className="heading1">{ title }</h1>
                    { back ? <Link className="goal btn btn-outline-white" to={"/user-intent/"}><i className="icon-back-goal mr-10"></i>Back to goal</Link> : '' }
                </div>
            </div>
       </header> 
    )
}

export default UIBanner;