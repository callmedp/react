import React, { useState } from 'react';
import { slide as Menu } from 'react-burger-menu';
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains'; 

const DefaultMenuNav = (props) =>{
    const {
        setType, setOpen, open
    } = props

    return (
        <Menu className='navigation' width={ '300px' } isOpen={open} onStateChange={state => setOpen(state.isOpen)}>
            <div className="m-guest-section">
                <figure className="micon-user-pic"></figure>
                <div className="media-body">
                <strong>Welcome Guest</strong>
                <p>
                    <Link className="btn-white-outline" to="{#}">Login</Link>
                    <Link className="btn-white-outline" to="{#}">Register</Link>
                </p>
                </div>
            </div>
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
                <a className="menu-item" href={`${siteDomain}/about-us`}>About us</a>
                <a className="menu-item" href={`${siteDomain}/contact-us`}>Contact us</a>
            </div>
        </Menu>
    );
}

export default DefaultMenuNav;