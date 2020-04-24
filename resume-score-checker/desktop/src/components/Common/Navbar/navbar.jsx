import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import * as Actions from '../../../store/LandingPage/actions/index';
import Loader from '../../../components/Loader/loader';
import { Toast } from '../../../services/Toast'
import './navbar.scss';
import { siteDomain } from '../../../utils/domains'
// getInformation

const Navbar = props => {
    const dispatch = useDispatch()
    const [flag, setFlag] = useState(false);
    const [candidateInfo, setCandidateInfo] = useState({});


    useEffect(() => {
        async function fetchUserInfo() {
            try {
                dispatch(Actions.getCartCount());
                const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({ resolve, reject })));
                if (isSessionAvailable['result']) {
                    // await dispatch(Actions.getCandidateId())
                    try {
                        setFlag(true);
                        const candidateInformation = await new Promise((resolve, reject) => dispatch(Actions.getCandidateInfo({ resolve, reject })))
                        setCandidateInfo(candidateInformation)
                        setFlag(false)
                    }
                    catch (e) {
                        setFlag(false);
                        Toast.fire({
                            icon: 'error',
                            html: '<h3>Something went wrong! Try again.<h3>'
                        })
                    }
                }
            }
            catch (e) {

            }
        }

        fetchUserInfo();
    }, []);


    const handleLogout = () => {
        localStorage.clear();
        window.location.href = `${siteDomain}/logout/?next=/resume-score-checker/`;
    }


    const cartScore = useSelector(state => state.scorePage && state.scorePage.cartCount);

    return (
        <React.Fragment>
            {flag && <Loader></Loader>}
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
                            <a className="nav-link dropdown-toggle" href="/#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span className="login-icon"></span></a>
                            {
                                candidateInfo && candidateInfo.candidateId ?
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        <a className="dropdown-item" href={`${siteDomain}/dashboard/`}>My Inbox</a>
                                        <a className="dropdown-item" href={`${siteDomain}/dashboard/myorder/`}>My orders</a>
                                        <a className="dropdown-item" href={`${siteDomain}/dashboard/mywallet/`}>My wallet</a>
                                        <span className="dropdown-item" >{candidateInfo.email}</span>
                                        <span className="dropdown-item" onClick={handleLogout}>logout</span>
                                    </div>
                                    : <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        <a className="dropdown-item" href={`${siteDomain}/login/?next=/resume-score-checker/`}>Login</a>
                                        <a className="dropdown-item" href={`${siteDomain}/register/?next=/resume-score-checker/`}>Register</a>
                                    </div>
                            }
                        </li>

                        <li className="d-flex align-items-center">
                            <a className="cart-icon" href= {`${siteDomain}/cart/payment-summary/`} >
                                <span className="cart-counter" id="cart-counter-id">{cartScore}</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </React.Fragment>
    );
}

export default Navbar;