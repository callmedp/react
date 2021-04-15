import React, { useState }  from 'react';
import './dashboardTabs.scss';
import { Link } from 'react-router-dom';
import { MyGA } from 'utils/ga.tracking.js';

   
const DashboardNavigation = (props) => {
    const { activeTab } = props
    return(
        <div className="m-db-tabs-wrap">
            <ul>
                <li>
                    <Link to={"/dashboard/"} className={activeTab === undefined ? 'active' : ''} onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_courses','', false, true)}>My Courses</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/myservices/"} className={activeTab === 'myservices' ? 'active' : ''} onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_services','', false, true)}>My Services</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/myorder/"} className={activeTab === 'myorder' ? 'active' : ''} onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_order','', false, true)}>My Orders</Link>
                </li>
                
                <li>
                    <Link to={"/dashboard/mywallet/"} className={activeTab === 'mywallet' ? 'active' : ''} onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_wallet','', false, true)}>My Wallet</Link>
                </li>
                
                {/* <li>
                    <Link to={"#"} className='active'>My Profile</Link>
                </li> */}
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;