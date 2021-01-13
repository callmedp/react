import React from 'react';
import './dashboardTabs.scss';
import { Link } from 'react-router-dom';

   
const DashboardNavigation = (props) => {
    return(
        <div className="m-db-tabs-wrap">
            <ul>
                <li>
                    <Link to={"#"} className="active">My Courses</Link>
                </li>
                
                <li>
                    <Link to={"#"} className="">My Services</Link>
                </li>
                
                <li>
                    <Link to={"#"} className="">My Order</Link>
                </li>
                
                <li>
                    <Link to={"#"} className="">My Wallet</Link>
                </li>
                
                <li>
                    <Link to={"#"} className="">My Profile</Link>
                </li>
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;