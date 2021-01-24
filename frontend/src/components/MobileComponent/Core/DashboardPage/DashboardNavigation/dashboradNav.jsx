import React, { useState }  from 'react';
import './dashboardTabs.scss';
import { Link } from 'react-router-dom';

   
const DashboardNavigation = (props) => {
    const { activeTab } = props
    return(
        <div className="m-db-tabs-wrap">
            <ul>
                <li>
                    <Link to={"/dashboard/my-courses"} className={activeTab === 'my-courses' ? 'active' : ''}>My Courses</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/my-services"} className={activeTab === 'my-services' ? 'active' : ''}>My Services</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/my-orders"} className={activeTab === 'my-orders' ? 'active' : ''}>My Orders</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/my-wallet"} className={activeTab === 'my-wallet' ? 'active' : ''}>My Wallet</Link>
                </li>
                
                {/* <li>
                    <Link to={"#"} className='active'>My Profile</Link>
                </li> */}
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;