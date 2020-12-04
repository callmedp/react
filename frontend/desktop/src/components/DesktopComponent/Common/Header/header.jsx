import React from 'react';
import { Link } from 'react-router-dom';
import './header.scss';
import { freeResourcesList, jobAssistanceList, categoryList, navSkillList } from 'utils/constants';
import { siteDomain } from 'utils/domains';
import DropDown from '../DropDown/dropDown';

const Header = (props) => {


    return (
        <div>
            <nav className="container-fluid padlr-0 shadow pos-rel zindex">
                <div className="container padlr-0">
                    <div className="navbar navbar-expand-lg navbar-light row">
                        <a className="navbar-brand" href={siteDomain}></a>
                        <div className="collapse navbar-collapse" id="navbarSupportedContent">
                            <form className="form-inline top-search my-2 my-lg-0 ml-auto">
                                <input className="form-control top-input" type="search" placeholder="Search anything" aria-label="Search" />
                                <button className="btn btn-search" type="submit"><figure className="icon-search"></figure></button>
                            </form>
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
                                        <Link className="dropdown-item" to={"#"}><strong>Call us:</strong> 0124-4312500/01</Link>
                                    </div>
                                </li>
                                <li className="nav-item dropdown dropdown-user">
                                    <Link className="nav-link link-ht" to={"#"} id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <figure className="icon-user"></figure>
                                    </Link>
                                    <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                                        <Link className="dropdown-item" to={"#"}>My Inbox</Link>
                                        <Link className="dropdown-item" to={"#"}>My Orders</Link>
                                        <Link className="dropdown-item" to={"#"}>My Wallet</Link>
                                        <Link className="dropdown-item" to={"#"}>My Referrals</Link>
                                        <Link className="dropdown-item" to={"#"}>abc@hindustantimes.com</Link>
                                        <div className="dropdown-divider"></div>
                                        <Link className="dropdown-item" to={"#"}>Logout</Link>
                                    </div>
                                </li>
                                <li className="nav-item position-relative">
                                    <span className="counter">4</span>
                                    <Link className="nav-link link-ht" to={"#"}>
                                        <figure className="icon-cart"></figure>
                                    </Link>
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
                                            <Link className="nav-link" to={skill.url}>{skill.name}</Link>
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