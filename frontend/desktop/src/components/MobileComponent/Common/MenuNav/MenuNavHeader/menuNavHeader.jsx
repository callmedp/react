import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';

const menuNavHeader = (props) => {
    const { candidateInfo, isLoggedIn } = props
    const handleLogout = () => {
        localStorage.clear();
        let path = window.location.pathname
        window.location.replace(`${siteDomain}/logout/?next=${path}`);
    }
    return(
        <>
        {
            isLoggedIn ? 
                <div className="m-guest-section">
                    <figure className="micon-user-pic"></figure>
                    <div className="media-body">
                        <strong>Welcome {candidateInfo?.first_name}</strong>
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
                            <a href={`${siteDomain}/login/`} className="btn-white-outline" >LogIn</a>
                            <a href={`${siteDomain}/register/`} className="btn-white-outline" >Register</a>
                        </p>
                    </div>
                </div>
        }
        </>
    )
}

export default menuNavHeader;