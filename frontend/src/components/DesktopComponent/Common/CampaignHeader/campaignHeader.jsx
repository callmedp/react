import React from 'react';
import { Link } from 'react-router-dom';
// import './header.scss';

const CampaignHeader = (props) => {
    const showTab = () => {
        console.log(this)
    }

    return (
        <div>
            <nav className="container-fluid padlr-0 shadow pos-rel zindex">
                <div className="container padlr-0">
                    <div className="navbar navbar-expand-lg navbar-light row">
                        <Link className="navbar-brand" to={"#"}></Link>
                    </div>
                </div>
            </nav>

            
        </div>
    )
} 

export default CampaignHeader;