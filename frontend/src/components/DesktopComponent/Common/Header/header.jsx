import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './header.scss';
import { freeResourcesList, jobAssistanceList, categoryList, navSkillList } from 'utils/constants';
import { siteDomain } from 'utils/domains';
import DropDown from './DropDown/dropDown';
import { useDispatch, useSelector } from 'react-redux';
import { cartCount, sessionAvailability, getCandidateInfo, fetchNavOffersAndTags } from 'store/Header/actions/index';
import { initLoggedInZendesk, loggedOutZendesk } from 'utils/zendeskIniti';
import { removeTrackingInfo } from 'utils/storage.js';
import SearchBar from './SeachBar/SearchBar';
import { MyGA } from 'utils/ga.tracking.js';

const Header = (props) => {

    const dispatch = useDispatch()
    const { count, navTags } = useSelector(store => store.header)
    const [candidateInfo, setCandidateInfo] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)

    const handleRedirect = (event, type) => {
        event.preventDefault();
        if( type === 'login'){
        MyGA.SendEvent('header_icons','ln_header_icons', 'ln_login', 'login','', false, true);
        }
        if( type === 'register'){
        MyGA.SendEvent('header_icons','ln_header_icons', 'ln_register', 'register','', false, true);
        }
        let redirectPath = window.location.pathname
        redirectPath ?
            window.location.href = `${siteDomain}/${type}/?next=${redirectPath}` :
            window.location.href = `${siteDomain}/${type}/`
    }

    const fetchUserInfo = async () => {
        try {
            dispatch(cartCount());
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));
            if (isSessionAvailable['result']) {
                try {
                    setIsLoggedIn(true)
                    const candidateId = isSessionAvailable['candidate_id']
                    const candidateInformation = await new Promise((resolve, reject) => dispatch(getCandidateInfo({candidateId, resolve, reject })))
                    initLoggedInZendesk(candidateInformation)
                    setCandidateInfo(candidateInformation)
                }
                catch (e) {
                    setIsLoggedIn(false)
                    console.log("ERROR OCCURED", e)
                }
            }
            else {
                setIsLoggedIn(false)
            }
        }

        catch (e) {
            setIsLoggedIn(false)
            console.log("ERROR OCCURED", e)
        }
    }

    useEffect(() => {
        fetchUserInfo();
        dispatch(fetchNavOffersAndTags());
    }, []);

    const handleLogout = () => {
        localStorage.clear();
        loggedOutZendesk();
        let path = window.location.pathname
        window.location.href = `${siteDomain}/logout/?next=${path}`;
    }

    const eventTracking = () => {
        MyGA.SendEvent('logo_click', 'ln_logo_click', 'ln_logo_click', 'homepage','',false, true)
        let product_tracking_mapping_id = localStorage.getItem("productTrackingMappingId");
        if(product_tracking_mapping_id == '10'){
            removeTrackingInfo()
        }
    }

    return (
        <div>
            <nav className="container-fluid padlr-0 shadow pos-rel zindex">
                <div className="container padlr-0">
                    <div className="navbar navbar-expand-lg navbar-light row">
                        <a className="navbar-brand" href={siteDomain} aria-label="brand logo" onClick={eventTracking}></a>
                        <div className="collapse navbar-collapse" id="navbarSupportedContent">
                            <SearchBar />
                            <ul className="navbar-nav navbar-right">
                                <li className="nav-item dropdown dropdown-jobs">
                                    <a className="nav-link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_job_assisstance', 'ln_job_assisstance', '', false, true) }>Job assistance</a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        {
                                            jobAssistanceList?.map((job) => <a key={job.url} className="dropdown-item" href={job.url} onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_job_assisstance', 'ln_'+job.id, '', false, true)}>{job.name}</a>)
                                        }
                                    </div>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href={`${siteDomain}/practice-tests/`} onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_practice_tests', 'ln_practice_tests', '', false, true)}>Practice test</a>
                                </li>
                                <li className="nav-item dropdown dropdown-resources">
                                    <a className="nav-link" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_free_resources', 'ln_free_resources', '', false, true)}>Free resources</a>
                                    <div className="dropdown-menu category-tab" aria-labelledby="navbarDropdown">
                                        <div className="resources-tab">

                                            <DropDown tabList={freeResourcesList} />

                                        </div>
                                    </div>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href={`${siteDomain}/talenteconomy/`} onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_blog', 'ln_blog', '', false, true)} >Blog</a>
                                </li>
                                
                                <li className="nav-item dropdown dropdown-user">
                                    <Link className="nav-link link-ht" aria-label="dropdown user link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <figure className="icon-user" onClick={ () => MyGA.SendEvent('header_icons','ln_header_icons', 'ln_account', 'loggedin_account','', false, true)}></figure>
                                    </Link>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        {
                                            isLoggedIn ? (
                                                <>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/`} >My Inbox</a>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/myorder/`}>My Orders</a>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/mywallet/`}>My Wallet</a>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/roundone/`}>My Referrals</a>
                                                    <a className="dropdown-item truncate" >{candidateInfo?.name ? candidateInfo?.name?.charAt(0)?.toUpperCase() + candidateInfo?.name?.slice(1) : candidateInfo?.email}</a>
                                                    <div className="dropdown-divider"></div>
                                                    <a className="dropdown-item" onClick={()=>handleLogout()} >Logout</a>
                                                </>
                                            ) : (
                                                    <>
                                                        <a className="dropdown-item" href={`${siteDomain}/login`} onClick={ (e) => handleRedirect(e,'login')}>Login</a>
                                                        <a className="dropdown-item" href={`${siteDomain}/register`} onClick={(e) => handleRedirect(e, 'register')}>Register</a>
                                                    </>
                                                )
                                        }
                                    </div>
                                </li>
                                <li className="nav-item dropdown dropdown-call">
                                    <Link className="nav-link link-ht" to={"#"} aria-label="dropdown call link" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <figure className="icon-call"></figure>
                                    </Link>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        <a className="dropdown-item" ><strong>Call us:</strong> 0124-4312500/01</a>
                                    </div>
                                </li>
                                <li className="nav-item position-relative">
                                    <span className="counter">{count}</span>
                                    <a className="nav-link link-ht" href={`${siteDomain}/cart/payment-summary/`} aria-label="payment cart button" onClick={() => MyGA.SendEvent('header_icons','ln_header_icons', 'ln_cart', 'cart','', false, true)}>
                                        <figure className="icon-cart"></figure>
                                    </a>
                                </li>
                            </ul>

                        </div>
                    </div>
                </div>
            </nav>

            <nav className="navbar-bg-light navbar navbar-expand-lg navbar-light">
                <div className="container">
                    <div className="row">
                        <ul className="navbar-nav" id="categories">
                            <li className="nav-item dropdown dropdown-categories">
                                <a className="nav-link" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <span className="sm-txt">Explore</span>Categories
                            <figure className="icon-down"></figure>
                                </a>
                                <div className="dropdown-menu category-tab" aria-labelledby="navbarDropdown">
                                    <div className="categories-tab">

                                        <DropDown tabList={categoryList} />

                                    </div>
                                </div>
                            </li>
                            {
                                navSkillList?.map((skill) => {
                                    return (
                                        <li key={skill.url} className="nav-item">
                                            <a className="nav-link" href={`${siteDomain}${skill.url}`} onClick={() => MyGA.SendEvent('navigation_menu','ln_navigation_menu', 'ln_'+skill.id+'_navigation', 'ln_'+skill.id, '', false, true)}>{skill.name}</a>
                                        </li>
                                    )
                                })
                            }
                            {
                                navTags?.map((tag, index) => {
                                    return (
                                        <li key={index} className="nav-item">
                                            <a href={`${siteDomain}${tag.skill_page_url}`} className="nav-link">{tag?.display_name}<small className="config-tag">{tag?.tag}</small></a>
                                        </li>
                                    )
                                })
                            }
                        </ul>
                    </div>
                </div>
            </nav>
        </div >
    )
}

export default Header;