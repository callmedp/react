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
                <a className="menu-item" href={`${siteDomain}/`} onClick={() => {setOpen(state => !state)}}><figure className="micon-home"></figure> Home</a>
                <a href="#/" className="menu-item" onClick={() => {setType('resumeServices')}}><figure className="micon-resume-service"></figure> Resume Services <figure className="micon-arrow-menusm ml-auto"></figure></a>
                <Link className="menu-item" to="{#}"><figure className="micon-linkedin-service"></figure> Linkedin Profile Writing</Link>
                <a href="#/" className="menu-item" onClick={() => setType('recruiterReach')}><figure className="micon-recruiter-service"></figure> Recruiter Reach <figure className="micon-arrow-menusm ml-auto"></figure></a>
                <a href="#/" className="menu-item" onClick={() => setType('freeResources')}><figure className="micon-free-resources"></figure> Free Resources <figure className="micon-arrow-menusm ml-auto"></figure></a>
                <a href="#/" className="menu-item" onClick={() => setType('otherServices')}><figure className="micon-other-services"></figure> Other Services <figure className="micon-arrow-menusm ml-auto"></figure></a>
                <a className="menu-item" href={`${siteDomain}/`}><figure className="micon-courses-services"></figure> Courses</a>
                <a className="menu-item" href={`${siteDomain}/talenteconomy/`}><figure className="micon-blog-services"></figure> Blog</a>
                <a className="menu-item" href={`${siteDomain}/about-us`}>About us</a>
                <a className="menu-item" href={`${siteDomain}/contact-us`}>Contact us</a>
            </div>
        </Menu>
    );
}

export default DefaultMenuNav;