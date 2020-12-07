import React, { useState, useEffect } from 'react';
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains'; 
import MenuNavHeader from '../MenuNavHeader/menuNavHeader';
import './defaultMenuNav.scss'
import { useSelector, useDispatch } from 'react-redux';
import { fetchNavOffersAndTags } from 'store/Common/Navigation/actions/index';


const DefaultMenuNav = (props) =>{
    const {
        setType, setOpen, open
    } = props
    const dispatch = useDispatch()

    const { navTags } = useSelector(store => store.navOffersAndTags)
    useEffect(() => {
        dispatch(fetchNavOffersAndTags())
    },[])

    return (
        <Menu className='navigation' width={ '300px' } isOpen={open} onStateChange={state => setOpen(state.isOpen)}>
            <MenuNavHeader />
            <div className="m-menu-links">
                <a className="menu-item" href={`${siteDomain}/`} onClick={() => {setOpen(state => !state)}}>
                    <figure className="micon-home" /> Home 
                </a>
                <a href="/" className="menu-item" onClick={(e) => {e.preventDefault();setType('allCourses')}}>
                    <figure className="micon-other-services" /> All Courses <figure className="micon-arrow-menusm ml-auto" />
                </a>
                <a href="/" className="menu-item" onClick={(e) => {e.preventDefault();setType('jobAssistanceServices')}}>
                    <figure className="micon-resume-service" /> Job Assistance Services <figure className="micon-arrow-menusm ml-auto" />
                </a>
                <Link className="menu-item" to="{#}"><figure className="micon-linkedin-service" /> Linkedin Profile Writing</Link>
                <a href="/" className="menu-item" onClick={(e) => {e.preventDefault();setType('freeResources')}}>
                    <figure className="micon-free-resources" /> Free Resources <figure className="micon-arrow-menusm ml-auto"/>
                </a>
                <a className="menu-item" href={`${siteDomain}/talenteconomy/`}>
                    <figure className="micon-blog-services" /> Blog
                </a>
                {
                    navTags?.length ? 
                    (
                        navTags.map((tag)=>{
                            return <a className="menu-item" href={`${siteDomain}${tag.skill_page_url}`}> {tag?.display_name}&emsp;<small class="m-config-tag">{tag?.tag}</small></a>
                        })
                    ) : null
                }
                {
                    // getDataStorage('candidate_id') && 
                    (
                        <ul className="dashboard-menu">
                            <li>
                                <a className="dashboard-menu--item" href="#/"><figure className="icon-dashboard" /> Dashboard</a>
                                <ul className="dashboard-menu__submmenu">
                                    <li><Link to="/dashboard/">Inbox</Link></li>
                                    <li><Link to="/dashboard/myorder/">My Order</Link></li>
                                    <li><Link to="/dashboard/mywallet/">My Wallet</Link></li>
                                </ul>
                            </li>
                        </ul>
                    )
                }
                <a className="menu-item" href={`${siteDomain}/about-us`}>About us</a>
                <a className="menu-item" href={`${siteDomain}/contact-us`}>Contact us</a>
            </div>
        </Menu>
    );
}

export default DefaultMenuNav;