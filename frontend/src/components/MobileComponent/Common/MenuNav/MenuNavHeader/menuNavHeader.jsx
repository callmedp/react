import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
import { loggedOutZendesk } from 'utils/zendeskIniti';

const menuNavHeader = (props) => {
    const { candidateInfo, isLoggedIn, sendLearningTracking } = props

    const handleLogout = () => {
        localStorage.clear();
        loggedOutZendesk();
        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_login_logout`,
            pageTitle: props.pageTitle,
            sectionPlacement:'menu_nav_header',
            eventCategory: 'login',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })
        let path = window.location.pathname
        window.location.href = `${siteDomain}/logout/?next=${path}`;
    }

    const handleRedirect = (type) => {
        let redirectPath = window.location.pathname

        sendLearningTracking({
            productId: '',
            event: `${props.pageTitle}_menu_nav_header_${type}`,
            pageTitle: props.pageTitle,
            sectionPlacement:'header',
            eventCategory: 'menu_nav_header',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: '',
        })

        redirectPath ?
            window.location.href = `${siteDomain}/${type}/?next=${redirectPath}` :
            window.location.href = `${siteDomain}/${type}/`
    }

    
    return(
        <>
        {
            isLoggedIn ? 
                <div className="m-guest-section">
                    <figure className="micon-user-pic"></figure>
                    <div className="media-body">
                        <strong>Welcome {candidateInfo?.name?.charAt(0)?.toUpperCase() + candidateInfo?.name?.slice(1)}</strong>
                        <p>
                            <a href="#" className="btn-white-outline" onClick={(e)=>{e.preventDefault();handleLogout()}}>Logout</a>
                        </p>
                    </div>
                </div>
            :
                <div className="m-guest-section">
                    <figure className="micon-user-pic"></figure>
                    <div className="media-body">
                        <strong>Welcome Guest</strong>
                        <p>
                            <a href='#' onClick={(e)=>{e.preventDefault();handleRedirect('login')}} className="btn-white-outline" >LogIn</a>
                            <a href='#' onClick={(e)=>{e.preventDefault();handleRedirect('register')}} className="btn-white-outline" >Register</a>
                        </p>
                    </div>
                </div>
        }
        </>
    )
}

export default menuNavHeader;