import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import * as Actions from '../../../stores/scorePage/actions/index';
import { eventClicked } from '../../../stores/googleAnalytics/actions/index'
import { Link } from 'react-router-dom';
import { Toast } from '../../../services/Toast'
import { menuData } from './menuData';
import './header.scss';
import { imageUrl, siteDomain } from '../../../Utils/domains';

export default function Header(props) {
    const [isSideBarOpen, setIsSideBarOpen] = useState(false)
    const [flag, setFlag] = useState(false);
    const dispatch = useDispatch()
    const [candidateInfo, setCandidateInfo] = useState({});

    const cartScore = useSelector(state => state.uploadFile ?.cartCount);

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
                        Toast('error', 'Something went wrong! Try again.')
                    }
                }
            }
            catch (e) {

            }
        }

        fetchUserInfo();
    }, []);
    const handleMenuButtonClick = () => {
        setIsSideBarOpen(!isSideBarOpen)
    };

    const handleLogout = () => {
        localStorage.clear();
        window.location.replace(`${siteDomain}/logout/?next=/resume-score-checker/`);
    }

    const handleCheckScoreClick = () => {
        dispatch(
            eventClicked({
                'action': 'M_CheckScore',
                'label': 'Header'
            })
        )
    }

    return (
        <div className="header">
            <div className="d-flex align-items-center">
                <span className="sprite header__barMenu mr-10" onClick={handleMenuButtonClick}></span>

                <a href={`${siteDomain}`} onClick={handleCheckScoreClick}>
                    <span className="header__logo">
                        <img src={`${imageUrl}score-checker/images/mobile/logo.svg`} alt="Header" />
                    </span>
                </a>
            </div>

            <a href={`${siteDomain}/cart/payment-summary/`} className="sprite icon-cart">
                <span>{cartScore}</span>
            </a>


            {/* {
                    ((props.page === 'homePage') && localStorage.getItem('resume_score')) ? (
                        <Link to="/resume-score-checker/score-checker" className="btn btn-md btn-outline-blue btn-round-30">
                            Check Score
                        </Link>
                    ) : null
                } */}

            {/* SideBar */}
            {menuData.length && (
                <nav className={`nav ${isSideBarOpen ? 'show' : ''}`}>
                    <div className="nav__loginWrap align-items-center">
                        <span className="nav__loginWrap__image mr-15">
                            <img src={`${imageUrl}score-checker/images/mobile/user-loggedin.jpg`} alt="" />
                        </span>

                        <div className="flex-1">
                            <h3>Welcome {candidateInfo && candidateInfo.name || 'Guest'}</h3>
                            {
                                candidateInfo && candidateInfo.candidateId ?

                                    <div className="mt-10 d-flex justify-content-between">
                                        <span onClick={handleLogout} className="py-5 btn btn-round-30 btn-outline-white px-20">Logout</span>
                                    </div>
                                    :
                                    <div className="mt-10 d-flex justify-content-between">
                                        <a href={`${siteDomain}/login/?next=/resume-score-checker/`}><div className="py-5 btn btn-round-30 btn-outline-white px-20">Login</div></a>
                                    </div>
                            }
                        </div>


                    </div>
                    <ul>
                        {menuData.map((item) =>
                            <li key={item.label}>
                                <a href={item.url}>
                                    <i className={item.icon}></i>
                                    {item.label}
                                </a>
                            </li>
                        )}
                    </ul>

                    <hr />

                    <div className="p-15">
                        <strong className="d-block">Call us:</strong>
                        <a className="d-block" href="tel:0124-4312500">0124-4312500/01</a>
                    </div>
                </nav>

            )}
            <div className={`overlay ${isSideBarOpen ? 'show' : ''}`} onClick={handleMenuButtonClick}></div>
        </div>
    );
}