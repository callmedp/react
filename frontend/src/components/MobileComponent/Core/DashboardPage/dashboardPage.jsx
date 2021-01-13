import React from 'react';
import './dashboardPage.scss';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import Footer from '../../Common/Footer/Footer';
import PopularCoursesSlider from '../../Common/PopularCoursesSlider/PopularCoursesSlider';
import HaveQuery from './HaveQuery/haveQuery';
import DashboardNavigation from './DashboardNavigation/dashboradNav';
import MyCourses from './MyCourses/myCourses';
import MyServices from './MyServices/myServices';
import MyOrders from './MyOrders/myOrders';
import MyWallet from './MyWallet/myWallet';
import MyProfile from './MyProfile/myProfile';
import PersonalDetail from './MyProfile/PersonalDetail';
import EditSkills from './MyProfile/EditSkills';

const Dashboard = () => {
    return(
        <div>
           <MenuNav />
           <header className="m-container m-header pb-0">
                <Header />
                <DashboardNavigation />
            </header>
            <main className="m-container">
                <MyCourses />
                {/* <MyServices /> */}
                {/* <MyOrders /> */}
                {/* <MyWallet /> */}
                {/* <MyProfile /> */}
                {/* <EditSkills /> */}
                {/* <PersonalDetail /> */}
                
                <PopularCoursesSlider />
                <HaveQuery />
            </main>
            
           <Footer /> 
        </div>
    )
}

export default Dashboard;