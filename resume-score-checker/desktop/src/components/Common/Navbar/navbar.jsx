import React from 'react';
import './navbar.scss';

const Navbar=props =>{
    return (
    <nav className="navbar navbar-expand-lg bg-light">
    <a className="navbar-brand" href="https://learning.shine.com/">&nbsp;</a>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav ml-auto">
            
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="/#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Courses</a>
                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="https://learning.shine.com/courses/sales-and-marketing/17/">Sales &amp; Marketing</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/operation-management/19/">Operation Management</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/banking-and-finance/20/">Banking &amp; Finance</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/it-information-technology/22/">Information Technology</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/hr-human-resource/25/">Human Resources</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/management/27/">Management</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/mass-communication/29/">Mass Communication</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/personal-development/21/">Personal Development</a>
                    <a className="dropdown-item" href="https://learning.shine.com/courses/law/23/">Law</a>
                    <a className="dropdown-item" href="https://learning.shine.com/online-courses.html">Course Catalogue</a>
                </div>
            </li>
            
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="/#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Job Assistance</a>
                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="https://learning.shine.com/services/resume-services/entry-level-freshers-4/pd-2553">International Resume</a>
                    <a className="dropdown-item" href="https://learning.shine.com/services/resume-services/entry-level-freshers/pd-2052">Visual Resume</a>
                    <a className="dropdown-item" href="https://learning.shine.com/services/professional-service/jobs-on-the-move-3/pd-3411">Jobs On The Move</a>
                    <a className="dropdown-item" href="https://learning.shine.com/services/linkedin-profile/180/">LinkedIn Profile</a>
                    <a className="dropdown-item" href="https://learning.shine.com/services/recruiter-connect/featured-profile-10/pd-1939">Featured Profile</a>
                    <a className="dropdown-item" href="https://learning.shine.com/services/recruiter-connect/application-highlighter-3/pd-4117">Application Highlighter</a>
                </div>
            </li>

            <li className="nav-item"><a className="nav-link" href="https://learning.shine.com/practice-tests/">Practice Tests</a></li>

       
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="/#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Free Resources</a>

                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="https://learning.shine.com/cms/resume-format/1/">Resume Formats</a>
                    <a className="dropdown-item" href="https://learning.shine.com/cms/resignation-letter-formats-samples/3/">Resignation Letter Formats</a>
                    <a className="dropdown-item" href="https://learning.shine.com/cms/cover-letter-format/7/">Cover Letter Formats</a>
                    <a className="dropdown-item" href="https://learning.shine.com/cms/resume-samples-and-templates/50/">Resume Templates</a>
                    <a className="dropdown-item" href="https://learning.shine.com/cms/linkedin-summary-examples/43/">LinkedIn Summary Example</a>
                    <a className="dropdown-item" href="https://learning.shine.com/cms/relieving-letter-format/58/">Relieving Letter</a>
                </div>
            </li>
            <li className="nav-item"><a className="nav-link" href="https://learning.shine.com/talenteconomy/">Blog</a></li>

            <li className="nav-item dropdown call-dropdown d-flex align-items-center">
                <a className="dropdown-toggle" href="/#" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"><span className="call-icon"></span></a>
                
                <div className="dropdown-menu">
                    <a className="dropdown-item text-center" href="tel:0124-4312500"><strong>Call us:</strong>0124-4312500/01</a>
                </div>
            </li>

            <li className="nav-item dropdown login-dropdown">
                <a className="nav-link dropdown-toggle" href="/#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="login-icon"></span></a>

                {/* <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="#">Resume Login</a>
                    <a className="dropdown-item" href="#">Register</a>
                </div> */}
                
                <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a className="dropdown-item" href="#">My Inbox</a>
                    <a className="dropdown-item" href="#">My orders</a>
                    <a className="dropdown-item" href="#">My wallet</a>
                    <a className="dropdown-item" href="#">priya.kharb@hindustantimes.com</a>
                    <a className="dropdown-item" href="#">logout</a>
                </div>
            </li>

            <li className="d-flex align-items-center">
                <a className="cart-icon" href="https://learning.shine.com/cart/payment-summary/">
                    <span className="" id="cart-counter-id"></span>
                </a>
            </li>
        </ul>
    </div>
</nav>
    );
}

export default Navbar;