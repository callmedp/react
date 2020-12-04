import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const menuNavHeader = () => {

    return(
        <>
        {
            true ? 
            (<div className="m-guest-section">
                <figure className="micon-user-pic"></figure>
                <div className="media-body">
                    {/* <strong>Welcome {candidate_detail?.first_name}</strong> */}
                    <strong>Welcome Gaurav</strong>
                    <p>
                        <Link className="btn-white-outline" to="{#}">Logout</Link>
                    </p>
                </div>
            </div>)
            :
            (<div className="m-guest-section">
                <figure className="micon-user-pic"></figure>
                <div className="media-body">
                    <strong>Welcome Guest</strong>
                    <p>
                        <Link className="btn-white-outline" to="{#}">SignIn</Link>
                        <Link className="btn-white-outline" to="{#}">Register</Link>
                    </p>
                </div>
            </div>)
        }
        </>
    )
}

export default menuNavHeader;