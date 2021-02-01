import React, { useState }  from 'react';
import './dashboardTabs.scss';
import { Link } from 'react-router-dom';

   
const DashboardNavigation = (props) => {
    const { activeTab } = props
    return(
        <div className="m-db-tabs-wrap">
            <ul>
                <li>
                    <Link to={"/dashboard/mycourses"} className={activeTab === 'mycourses' ? 'active' : ''}>My Courses</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/myservices"} className={activeTab === 'myservices' ? 'active' : ''}>My Services</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/myorder"} className={activeTab === 'myorder' ? 'active' : ''}>My Orders</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/mywallet"} className={activeTab === 'mywallet' ? 'active' : ''}>My Wallet</Link>
                </li>
                
                {/* <li>
                    <Link to={"#"} className='active'>My Profile</Link>
                </li> */}
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;