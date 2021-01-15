import React from 'react';
import './dashboardPage.scss';
import Header from '../../Common/Header/header';
import Footer from '../../Common/Footer/footer';
import PopularCourses from './PopularSourses/PopularCourses';
import DashboardNavigation from './DashboardNavigation/DashboardTabs';
import HaveQuery from './HaveQuery/HaveQuery';
import BreadCrumbs from './Breadcrumb/Breadcrumb';
import MyCourses from './MyCourses/myCourses';
import MyServices from './MyServices/myServices';
import MyOrders from './MyOrders/myOrders';
import MyWallet from './MyWallet/myWallet';
import MyProfile from './MyProfile/myProfile';
import FAQ from './FAQ/faq';

const Dashboard = (props) => {
    console.log("props are", props);
    return(
        <div>
           <Header />
            <main>

                <div className="container">
                    <BreadCrumbs />
                    
                    <div className="dashboard-warp">
                        <div className="dashboard-warp--tab">
                            <DashboardNavigation />
                        </div>

                        <div className="dashboard-warp--wrap">
                            <div className="dashboard-warp--content">
                                {/* <MyOrders /> */}
                            </div>
                        </div>

                    </div>
                </div>
                <HaveQuery />
                <PopularCourses />

                
                
                {/* <MyServices /> */}
                {/* <MyOrders /> */}
                {/* <MyWallet /> */}
                {/* <MyProfile /> */}
                {/* <FAQ /> */}
                
            </main>

           
           <Footer /> 
        </div>
    )
}

export default Dashboard;