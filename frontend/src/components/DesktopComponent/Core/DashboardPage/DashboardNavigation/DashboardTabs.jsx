import React from 'react';
import './dashboardTabs.scss';
import { NavLink } from 'react-router-dom';
import { MyGA } from 'utils/ga.tracking.js';

   
const DashboardNavigation = (props) => {
    return(
        <div className="db-tabs-wrap">
            <ul>
                <li>
                    <NavLink activeClassName="active" exact={true} to={"/dashboard/"} className="my-courses" onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_courses','', false, true)}>
                        <span className="d-block">My Courses</span>
                    </NavLink>
                </li>
                
                <li>
                    <NavLink activeClassName="active" to={"/dashboard/myservices/"} className="my-services" onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_services','', false, true)}>
                        <span className="d-block">My Services</span>
                    </NavLink>
                </li>
                
                <li>
                    <NavLink activeClassName="active" to={"/dashboard/myorder/"} className="my-order" onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_orders','', false, true)}>
                        <span className="d-block">My Orders</span>
                    </NavLink>
                </li>
                
                <li>
                    <NavLink activeClassName="active" to={'/dashboard/mywallet/'} className="my-wallet" onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_wallet','', false, true)}>
                        <span className="d-block">My Wallet</span>
                    </NavLink>
                </li>
                
                {/* <li>
                    <NavLink activeClassName="active" to={"/dashboard/myprofile/"} className="my-profile" onClick={() => MyGA.SendEvent('DashboardLeftMenu','ln_dashboard_left_menu', 'ln_click_menu_name', 'my_profile','', false, true)}>
                        <span className="d-block">My Profile</span>
                    </NavLink>
                </li> */}
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;