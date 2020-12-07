import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const menuNavHeader = (props) => {
    const { candidateInfo, isLoggedIn } = props
    
    return(
        <>
        {
            isLoggedIn ? 
                <div className="m-guest-section">
                    <figure className="micon-user-pic"></figure>
                    <div className="media-body">
                        <strong>Welcome {candidateInfo?.first_name}</strong>
                        <p>
                            <Link className="btn-white-outline" to="{#}">Logout</Link>
                        </p>
                    </div>
                </div>
            :
                <div className="m-guest-section">
                    <figure className="micon-user-pic"></figure>
                    <div className="media-body">
                        <strong>Welcome Guest</strong>
                        <p>
                            <Link className="btn-white-outline" to="{#}">SignIn</Link>
                            <Link className="btn-white-outline" to="{#}">Register</Link>
                        </p>
                    </div>
                </div>
        }
        </>
    )
}

export default menuNavHeader;