import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './header.scss';
import { freeResourcesList, jobAssistanceList, categoryList, navSkillList } from 'utils/constants';
import { siteDomain } from 'utils/domains';
import DropDown from './DropDown/dropDown';
import { useDispatch, useSelector } from 'react-redux';
import { cartCount, fetchNavOffersAndTags } from 'store/Header/actions/index';
import { initLoggedInZendesk, loggedOutZendesk } from 'utils/zendeskIniti';
import { removeTrackingInfo, getCandidateInformation,getCandidateId } from 'utils/storage.js';
import SearchBar from './SeachBar/SearchBar';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';


const Header = (props) => {
    const dispatch = useDispatch()
    const { count, navTags } = useSelector(store => store.header)
    const [candidateInfo, setCandidateInfo] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const { isHomepage, isUserIntentPage, showMainOffer, setShowMainOffer } = props;
    const sendLearningTracking = useLearningTracking();

    const handleRedirect = (event, type) => {
        event.preventDefault();
        if (type === 'login') {
            MyGA.SendEvent('header_icons', 'ln_header_icons', 'ln_account', 'login', '', false, true);
            sendLearningTracking({
                productId: '',
                event: `${props.pageTitle}_login_login`,
                pageTitle: props.pageTitle,
                sectionPlacement:'header',
                eventCategory: 'login',
                eventLabel: '',
                eventAction: 'click',
                algo: '',
                rank: '',
            })
        }
        if (type === 'register') {
            MyGA.SendEvent('header_icons', 'ln_header_icons', 'ln_account', 'register', '', false, true);
            sendLearningTracking({
                productId: '',
                event: `${props.pageTitle}_login_register`,
                pageTitle: props.pageTitle,
                sectionPlacement:'header',
                eventCategory: 'login',
                eventLabel: '',
                eventAction: 'click',
                algo: '',
                rank: '',
            })
        }
        let redirectPath = props.location?.pathname;
        redirectPath ?
            window.location.href = `${siteDomain}/${type}/?next=${redirectPath}` :
            window.location.href = `${siteDomain}/${type}/`
    }

    const fetchUserInfo = async () => {
        try {
            dispatch(cartCount());
        
            if (getCandidateId()){
                try {
                    setIsLoggedIn(true)
                    // const candidateId = getCandidateId()
                    // const candidateInformation = await new Promise((resolve, reject) => dispatch(getCandidateInfo({ candidateId, resolve, reject })))
                    const candidateInformation = getCandidateInformation()
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
        sessionStorage.clear();
        loggedOutZendesk();
        let path = window.location.pathname
        window.location.href = `${siteDomain}/logout/?next=${path}`;
    }

    const eventTracking = () => {
        MyGA.SendEvent('logo_click', 'ln_logo_click', 'ln_logo_click', 'homepage', '', false, true)
        let product_tracking_mapping_id = localStorage.getItem("productTrackingMappingId");
        if (product_tracking_mapping_id == '10') {
            removeTrackingInfo()
        }
        
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_learning_logo_homepage_redirection`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'learning_logo',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const jobAssistanceTracking = (job, index) => {
        MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_job_assisstance', 'ln_' + job.id, '', false, true)
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_job_assistance_${job.id}`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'job_assistance',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: index,
        })
    }

    const practiceTestTracking = () =>{
        MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_practice_tests', 'ln_practice_tests', '', false, true)
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_practice_test_redirection`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'practice_test',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const blogTracking = () => {
        MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_blog', 'ln_blog', '', false, true)
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_blog_redirection`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'blog',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const handleHeaderTracking = (category, event) => {
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_${category}_${event}`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: category,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const callUsTracking = () => {
        MyGA.SendEvent('header_icons', 'ln_header_icons', 'ln_call', 'tel:0124-6096096/97', '', false, true);
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_call_us`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'call_us',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const cartTracking = () => {
        MyGA.SendEvent('header_icons', 'ln_header_icons', 'ln_cart', 'cart', '', false, true);
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_add_to_cart_redirection`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'add_to_cart',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    const navTracking = (type, id) => {
        if(type === 'navSkillList'){
            MyGA.SendEvent('navigation_menu', 'ln_navigation_menu', 'ln_' + id + '_navigation', 'ln_' + id, '', false, true);
        }
        
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_nav_list_${id}`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'nav_list',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
    }

    return (
        <div>
            <nav className="container-fluid padlr-0 shadow pos-rel zindex">
                <div className="container padlr-0">
                    <div className="navbar navbar-expand-lg navbar-light row">
                        <Link className="navbar-brand" itemScope itemType="http://schema.org/Organization" to="/" aria-label="brand logo" onClick={eventTracking}>
                            <meta itemProp="name" content="Shine"/>
                            <meta itemProp="url" content={`${siteDomain}`} />
                        </Link>

                            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                                { !isHomepage ? <SearchBar place="topHeader" placeHolder = {props.placeHolder} isHomepage={isHomepage} pageTitle={''} /> : ''}
                                <ul className={`navbar-nav navbar-right ${ !!isHomepage ? ' ml-auto' : ''}`}>
                                    <li className="nav-item dropdown dropdown-jobs">
                                        <a className="nav-link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" onClick={() => MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_job_assisstance', 'ln_job_assisstance', '', false, true)}>Job assistance</a>
                                        <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                            {
                                                jobAssistanceList?.map((job, index) => <a key={job.url} className="dropdown-item" href={job.url} onClick={() => jobAssistanceTracking(job, index)}>{job.name}</a>)
                                            }
                                        </div>
                                    </li>
                                    <li className="nav-item">
                                        <a className="nav-link" href={`${siteDomain}/practice-tests/`} onClick={practiceTestTracking}>Practice test</a>
                                    </li>
                                    <li className="nav-item dropdown dropdown-resources">
                                        <a className="nav-link" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" onClick={() => MyGA.SendEvent('homepage_navigation', 'ln_homepage_navigation', 'ln_free_resources', 'ln_free_resources', '', false, true)}>Free resources</a>
                                        <div className="dropdown-menu category-tab" aria-labelledby="navbarDropdown">
                                            <div className="resources-tab">

                                                <DropDown usedIn="freeResources" pageTitle = {props.pageTitle} tabList={freeResourcesList} />

                                            </div>
                                        </div>
                                    </li>
                                    <li className="nav-item">
                                        <a className="nav-link" href={`${siteDomain}/talenteconomy/`} onClick={blogTracking} >Blog</a>
                                    </li>
                                    <li className="nav-item dropdown dropdown-user">
                                        <Link className="nav-link link-ht" aria-label="dropdown user link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <figure className="icon-user" onClick={() => MyGA.SendEvent('header_icons', 'ln_header_icons', 'ln_account', 'loggedin_account', '', false, true)}></figure>
                                        </Link>
                                        <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                            {
                                                isLoggedIn ? (
                                                    <>
                                                        <a className="dropdown-item" onClick={() => handleHeaderTracking('login', 'my_courses')} href={`${siteDomain}/dashboard/`} >My Courses</a>
                                                        <a className="dropdown-item" onClick={() => handleHeaderTracking('login', 'my_services')} href={`${siteDomain}/dashboard/myservices`} >My Services</a>
                                                        <a className="dropdown-item" onClick={() => handleHeaderTracking('login', 'my_orders')} href={`${siteDomain}/dashboard/myorder/`}>My Orders</a>
                                                        <a className="dropdown-item" onClick={() => handleHeaderTracking('login', 'my_wallets')} href={`${siteDomain}/dashboard/mywallet/`}>My Wallet</a>
                                                        <a className="dropdown-item" onClick={() => handleHeaderTracking('login', 'my_referrals')} href={`${siteDomain}/dashboard/roundone/`}>My Referrals</a>
                                                        <a className="dropdown-item truncate" >{candidateInfo?.email ? candidateInfo?.email : candidateInfo?.name?.charAt(0)?.toUpperCase() + candidateInfo?.name?.slice(1)}</a>
                                                        <div className="dropdown-divider"></div>
                                                        <a className="dropdown-item" onClick={() => {handleHeaderTracking('login', 'logout');handleLogout()}} >Logout</a>
                                                    </>
                                                ) : (
                                                        <>
                                                            <a className="dropdown-item" href={`${siteDomain}/login`} onClick={(e) => handleRedirect(e, 'login')}>Login</a>
                                                            <a className="dropdown-item" href={`${siteDomain}/register`} onClick={(e) => handleRedirect(e, 'register')}>Register</a>
                                                        </>
                                                    )
                                            }
                                        </div>
                                    </li>
                                    <li className="nav-item dropdown dropdown-call">
                                        <Link className="nav-link link-ht" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <figure className="icon-call" onClick={callUsTracking}></figure>
                                        </Link>
                                        <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                            <a className="dropdown-item" onClick={callUsTracking}><strong>Call us:</strong> 0124-6096096/97</a>
                                        </div>
                                    </li>
                                    <li className="nav-item position-relative">
                                        <span className="counter">{count}</span>
                                        <a className="nav-link link-ht" href={`${siteDomain}/cart/payment-summary/`} aria-label="payment cart button" onClick={cartTracking}>
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

                                            <DropDown pageTitle = {props.pageTitle} usedIn="exploreCategories" tabList={categoryList} />

                                        </div>
                                    </div>
                                </li>
                                {
                                    navSkillList?.map((skill) => {
                                        return (
                                            <li key={skill.url} className="nav-item">
                                                <Link className="nav-link" to={`${skill.url}`} onClick={() => navTracking('navSkillList', skill.id)}>{skill.name}</Link>
                                            </li>
                                        )
                                    })
                                }
                                {
                                    navTags?.map((tag, index) => {
                                        return (
                                            <li key={index} className="nav-item">
                                                <a href={tag.skill_page_url} className="nav-link"  onClick={() => navTracking('navTags', tag.display_name)} >{tag?.display_name}   
                                                    <small className="config-tag">{tag?.tag}
                                                    </small>
                                                </a>
                                            </li>
                                        )
                                    })
                                }
                            </ul>
                        </div>
                        {
                            isHomepage || isUserIntentPage ? '' : 
                                <span className="ui-btn">
                                    <Link to={"/user-intent"} className="btn btn-gradient"><figure className="icon-ui-cg"></figure> GET CAREER GUIDANCE <span>NEW</span></Link>
                                </span>
                        }
                    </div>
                    { (!showMainOffer && isHomepage) && <a onClick={() => setShowMainOffer(true)} className="icon-offer ml-auto mr-20 cursorLink" data-toogle="tooltip" title="View Offer"></a> }
                </nav>
        </div >
    )
}

export default Header;