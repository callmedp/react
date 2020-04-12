import React from 'react';
import './navbar.scss';

const Navbar=props=>{
    return (
    <nav className="navbar navbar-expand-lg bg-light">
    <a className="navbar-brand" href="#"></a>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav ml-auto">
            
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Courses</a>
                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="#">Sales &amp; Marketing</a>
                    <a className="dropdown-item" href="#">Operation Management</a>
                    <a className="dropdown-item" href="#">Banking &amp; Finance</a>
                    <a className="dropdown-item" href="#">Information Technology</a>
                    <a className="dropdown-item" href="#">Human Resources</a>
                    <a className="dropdown-item" href="#">Management</a>
                    <a className="dropdown-item" href="#">Mass Communication</a>
                    <a className="dropdown-item" href="#">Personal Development</a>
                    <a className="dropdown-item" href="#">Law</a>
                    <a className="dropdown-item" href="#">Course Catalogue</a>
                </div>
            </li>
            
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Job Assistance</a>
                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="#">International Resume</a>
                    <a className="dropdown-item" href="#">Visual Resume</a>
                    <a className="dropdown-item" href="#">Jobs On The Move</a>
                    <a className="dropdown-item" href="#">LinkedIn Profile</a>
                    <a className="dropdown-item" href="#">Featured Profile</a>
                    <a className="dropdown-item" href="#">Application Highlighter</a>
                </div>
            </li>

            <li className="nav-item"><a className="nav-link" href="#">Practice Tests</a></li>

       
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Free Resources</a>

                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="#">Resume Formats</a>
                    <a className="dropdown-item" href="#">Resignation Letter Formats</a>
                    <a className="dropdown-item" href="#">Cover Letter Formats</a>
                    <a className="dropdown-item" href="#">Resume Templates</a>
                    <a className="dropdown-item" href="#">LinkedIn Summary Example</a>
                    <a className="dropdown-item" href="#">Relieving Letter</a>
                </div>
            </li>
            <li className="nav-item"><a className="nav-link" href="#">Blog</a></li>

            <li className="nav-item dropdown call-dropdown mr-4 d-flex align-items-center">
                <a className="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span className="call-icon"></span></a>
                
                <div className="dropdown-menu">
                    <a className="dropdown-item text-center" href="tel:0124-4312500"><strong>Call us:</strong>0124-4312500/01</a>
                </div>
            </li>
            
            <li className="mr-4 d-flex align-items-center"><a className="login-icon"></a> </li>

            <li className="d-flex align-items-center">
                <a className="cart-icon" href="#">
                    <span className="" id="cart-counter-id"></span>
                </a>
            </li>
        </ul>
    </div>
</nav>
    );
}

export default  Navbar;