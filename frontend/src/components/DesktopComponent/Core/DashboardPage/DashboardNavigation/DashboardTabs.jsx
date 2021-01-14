import React from 'react';
import './dashboardTabs.scss';
import { Link } from 'react-router-dom';

   
const DashboardNavigation = (props) => {
    return(
        <div className="db-tabs-wrap">
            <ul>
                <li>
                    <Link to={"#"} className="my-courses ">
                        <span className="d-block">My Courses</span>
                    </Link>
                </li>
                
                <li>
                    <Link to={"#"} className="my-services">
                        <span className="d-block">My Services</span>
                    </Link>
                </li>
                
                <li>
                    <Link to={"#"} className="my-order active">
                        <span className="d-block">My Order</span>
                    </Link>
                </li>
                
                <li>
                    <Link to={"#"} className="my-wallet">
                        <span className="d-block">My Wallet</span>
                    </Link>
                </li>
                
                <li>
                    <Link to={"#"} className="my-profile">
                        <span className="d-block">My Profile</span>
                    </Link>
                </li>
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;