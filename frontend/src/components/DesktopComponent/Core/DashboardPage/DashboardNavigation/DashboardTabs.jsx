import React from 'react';
import './dashboardTabs.scss';
import { NavLink } from 'react-router-dom';

   
const DashboardNavigation = (props) => {
    return(
        <div className="db-tabs-wrap">
            <ul>
                <li>
                    <NavLink activeClassName="active" exact={true} to={"/dashboard/mycourses/"} className="my-courses">
                        <span className="d-block">My Courses</span>
                    </NavLink>
                </li>
                
                <li>
                    <NavLink activeClassName="active" to={"/dashboard/myservices/"} className="my-services">
                        <span className="d-block">My Services</span>
                    </NavLink>
                </li>
                
                <li>
                    <NavLink activeClassName="active" to={"/dashboard/myorder/"} className="my-order">
                        <span className="d-block">My Order</span>
                    </NavLink>
                </li>
                
                <li>
                    <NavLink activeClassName="active" to={'/dashboard/mywallet/'} className="my-wallet">
                        <span className="d-block">My Wallet</span>
                    </NavLink>
                </li>
                
                {/* <li>
                    <NavLink activeClassName="active" to={"/dashboard/myprofile/"} className="my-profile">
                        <span className="d-block">My Profile</span>
                    </NavLink>
                </li> */}
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;