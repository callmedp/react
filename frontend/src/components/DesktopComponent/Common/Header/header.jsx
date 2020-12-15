import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './header.scss';
import { freeResourcesList, jobAssistanceList, categoryList, navSkillList } from 'utils/constants';
import { siteDomain } from 'utils/domains';
import DropDown from './DropDown/dropDown';
import { useDispatch, useSelector } from 'react-redux';
import { cartCount, sessionAvailability, getCandidateInfo, fetchNavOffersAndTags } from 'store/Header/actions/index';
import zendeskInit from 'utils/zendeskIniti';
import AsyncExample from './search';
import TypeAhead from './Typeahead';

const Header = (props) => {

    const dispatch = useDispatch()
    const { count, navTags } = useSelector(store => store.header)
    const [candidateInfo, setCandidateInfo] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)



    const fetchUserInfo = async () => {
        try {
            dispatch(cartCount());
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(sessionAvailability({ resolve, reject })));

            if (isSessionAvailable['result']) {
                try {
                    setIsLoggedIn(true)
                    const candidateInformation = await new Promise((resolve, reject) => dispatch(getCandidateInfo({ resolve, reject })))
                    setCandidateInfo(candidateInformation)
                    zendeskInit(candidateInformation)
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
        window.location.replace(`${siteDomain}/logout/?next=/resume-score-checker/`);
    }

    return (
        <div>
            <nav className="container-fluid padlr-0 shadow pos-rel zindex">
                <div className="container padlr-0">
                    <div className="navbar navbar-expand-lg navbar-light row">
                        <a className="navbar-brand" href={siteDomain}></a>
                        <div className="collapse navbar-collapse" id="navbarSupportedContent">
                            <TypeAhead />
                            <ul className="navbar-nav navbar-right">
                                <li className="nav-item dropdown dropdown-jobs">
                                    <a className="nav-link" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Job assistance</a>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        {
                                            jobAssistanceList?.map((job) => <a key={job.url} className="dropdown-item" href={job.url} >{job.name}</a>)
                                        }
                                    </div>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href={`${siteDomain}/practice-tests/`}>Practice test</a>
                                </li>
                                <li className="nav-item dropdown dropdown-resources">
                                    <a className="nav-link" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Free resources</a>
                                    <div className="dropdown-menu category-tab" aria-labelledby="navbarDropdown">
                                        <div className="resources-tab">

                                            <DropDown tabList={freeResourcesList} />

                                        </div>
                                    </div>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href={`${siteDomain}/talenteconomy/`} >Blog</a>
                                </li>
                                <li className="nav-item dropdown dropdown-call">
                                    <Link className="nav-link link-ht" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <figure className="icon-call"></figure>
                                    </Link>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        <a className="dropdown-item" ><strong>Call us:</strong> 0124-4312500/01</a>
                                    </div>
                                </li>
                                <li className="nav-item dropdown dropdown-user">
                                    <Link className="nav-link link-ht" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <figure className="icon-user"></figure>
                                    </Link>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        {
                                            isLoggedIn ? (
                                                <>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/`} >My Inbox</a>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/myorder/`}>My Orders</a>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/mywallet/`}>My Wallet</a>
                                                    <a className="dropdown-item" href={`${siteDomain}/dashboard/roundone/`}>My Referrals</a>
                                                    <a className="dropdown-item"  >abc@hindustantimes.com</a>
                                                    <div className="dropdown-divider"></div>
                                                    <a className="dropdown-item" onClick={handleLogout} >Logout</a>
                                                </>
                                            ) : (
                                                    <>
                                                        <a className="dropdown-item" href={`${siteDomain}/login`}>Login</a>
                                                        <a className="dropdown-item" href={`${siteDomain}/register`}>Register</a>
                                                    </>
                                                )
                                        }
                                    </div>
                                </li>
                                <li className="nav-item position-relative">
                                    <span className="counter">{count}</span>
                                    <a className="nav-link link-ht" href={`${siteDomain}/cart/payment-summary/`}>
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
                                            <a className="nav-link" href={`${siteDomain}${skill.url}`}>{skill.name}</a>
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