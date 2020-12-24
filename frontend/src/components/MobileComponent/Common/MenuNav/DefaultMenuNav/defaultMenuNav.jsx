import React, { useState, useEffect } from 'react';
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';
import { siteDomain, resumeShineSiteDomain } from 'utils/domains'; 
import MenuNavHeader from '../MenuNavHeader/menuNavHeader';
import './defaultMenuNav.scss'
import { useSelector, useDispatch } from 'react-redux';
import { cartCount, sessionAvailability, getCandidateInfo, fetchNavOffersAndTags } from 'store/Header/actions/index';
import { initLoggedInZendesk } from 'utils/zendeskIniti';
import { trackUser } from 'store/Tracking/actions/index.js';
import { removeTrackingInfo } from 'utils/storage.js';
import { MyGA } from 'utils/ga.tracking.js';

const DefaultMenuNav = (props) =>{
    const {
        setType, setOpen, open
    } = props
    const dispatch = useDispatch()

    const { navTags } = useSelector(store => store.header)
    const [candidateInfo, setCandidateInfo] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)

    const fetchUserInfo = async () => {
        try {
            dispatch(cartCount());
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));

            if (isSessionAvailable['result']) {
                try {
                    setIsLoggedIn(true)
                    const candidateId = isSessionAvailable['candidate_id']
                    const candidateInformation = await new Promise((resolve, reject) => dispatch(getCandidateInfo({candidateId, resolve, reject })))
                    initLoggedInZendesk(candidateInformation, true)
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

    const eventTracking = () => {
        MyGA.SendEvent('logo_click', 'ln_logo_click', 'ln_logo_click', 'homepage','',false, true)
        let product_tracking_mapping_id = localStorage.getItem("productTrackingMappingId");
        if(product_tracking_mapping_id == '10'){
            removeTrackingInfo()
        }
    }

    useEffect(() => {
        fetchUserInfo();
        dispatch(fetchNavOffersAndTags());
    },[])

    return (
        <Menu className='navigation' width={ '300px' } isOpen={open} onStateChange={state => setOpen(state.isOpen)}>
            <MenuNavHeader isLoggedIn={isLoggedIn} candidateInfo={candidateInfo}/>
            <div className="m-menu-links">
                <a className="menu-item" href={`${siteDomain}/`} onClick={() => {setOpen(state => !state);eventTracking()}}>
                    <figure className="micon-home" /> Home 
                </a>
                <a href="/" className="menu-item" onClick={(e) => {e.preventDefault();setType('allCourses')}}>
                    <figure className="micon-courses-services" /> All Courses <figure className="micon-arrow-menusm ml-auto" />
                </a>
                <a href="/" className="menu-item" onClick={(e) => {e.preventDefault();setType('jobAssistanceServices'); MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_job_assisstance', 'ln_job_assisstance', '', false, true)} }>
                    <figure className="micon-resume-service" /> Job Assistance Services <figure className="micon-arrow-menusm ml-auto" />
                </a>
                <a href={`${resumeShineSiteDomain}/product/linkedin-profile-writing/entry-level-2/1926/`} className="menu-item" onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_linked_profile_writing', 'ln_linked_profile_writing', '', false, true)} ><figure className="micon-linkedin-service" /> Linkedin Profile Writing</a>
                <a href="/" className="menu-item" onClick={(e) => {e.preventDefault();setType('freeResources'); MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_free_resources', 'ln_free_resources', '', false, true)}}>
                    <figure className="micon-free-resources" /> Free Resources <figure className="micon-arrow-menusm ml-auto"/>
                </a>
                <a className="menu-item" href={`${siteDomain}/talenteconomy/`} onClick={() => MyGA.SendEvent('homepage_navigation','ln_homepage_navigation', 'ln_blog', 'ln_blog', '', false, true)}>
                    <figure className="micon-blog-services" /> Blog
                </a>
                {
                    navTags?.length ? 
                    (
                        navTags.map((tag, index)=>{
                            return <a key={index} className="menu-item" href={`${siteDomain}${tag.skill_page_url}`}> {tag?.display_name}&emsp;<small className="m-config-tag">{tag?.tag}</small></a>
                        })
                    ) : null
                }
                {
                    isLoggedIn && 
                    (
                        <ul className="dashboard-menu">
                            <li>
                                <a className="dashboard-menu--item" href={`${siteDomain}/dashboard/`}><figure className="icon-dashboard" /> Dashboard</a>
                                <ul className="dashboard-menu__submmenu">
                                    <li><a href={`${siteDomain}/dashboard/`}>Inbox</a></li>
                                    <li><a href={`${siteDomain}/dashboard/myorder/`}>My Order</a></li>
                                    <li><a href={`${siteDomain}/dashboard/mywallet/`}>My Wallet</a></li>
                                </ul>
                            </li>
                        </ul>
                    )
                }
                <a className="menu-item" href={`${siteDomain}/about-us`} onClick={() => MyGA.SendEvent('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'About Us','', false, true)}>About us</a>
                <a className="menu-item" href={`${siteDomain}/contact-us`} onClick={() =>  MyGA.SendEvent('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Contact Us','', false, true)}>Contact us</a>
            </div>
        </Menu>
    );
}

export default DefaultMenuNav;