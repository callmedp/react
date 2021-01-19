import React, { useState }  from 'react';
import './dashboardTabs.scss';
import { Link } from 'react-router-dom';

   
const DashboardNavigation = (props) => {
    const {
        activeTab, setActiveTab
    } = props

    const showTab = (tabType) => {
        setActiveTab(tabType)
    }

    return(
        <div className="m-db-tabs-wrap">
            <ul>
                <li>
                    <Link to={"#"} className={activeTab === 'Courses' ? 'active' : ''}  onClick={() => showTab('Courses')}>My Courses</Link>
                </li>
                
                <li>
                    <Link to={"#"} className={activeTab === 'Services' ? 'active' : ''} onClick={() => showTab('Services')}>My Services</Link>
                </li>
                
                <li>
                    <Link to={"#"} className={activeTab === 'Orders' ? 'active' : ''} onClick={() => showTab('Orders')}>My Orders</Link>
                </li>
                
                <li>
                    <Link to={"#"} className={activeTab === 'Wallet' ? 'active' : ''} onClick={() => showTab('Wallet')}>My Wallet</Link>
                </li>
                
                <li>
                    <Link to={"#"} className={activeTab === 'Profile' ? 'active' : ''} onClick={() => showTab('Profile')}>My Profile</Link>
                </li>
            </ul>
        </div>
    )
}
   
export default DashboardNavigation;