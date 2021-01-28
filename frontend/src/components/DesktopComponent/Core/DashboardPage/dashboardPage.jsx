import React, {useState, useEffect} from 'react';
import './dashboardPage.scss';
import Header from '../../Common/Header/header';
import Footer from '../../Common/Footer/footer';
import PopularCourses from './PopularCourses/PopularCourses';
import DashboardNavigation from './DashboardNavigation/DashboardTabs';
import HaveQuery from './HaveQuery/HaveQuery';
import BreadCrumbs from './Breadcrumb/Breadcrumb';
import MyCourses from './MyCourses/myCourses';
import MyServices from './MyServices/myServices';
import MyOrders from './MyOrders/myOrders';
import MyWallet from './MyWallet/myWallet';
import MyProfile from './MyProfile/myProfile';
import FAQ from './FAQ/faq';
// import { useDispatch, useSelector } from 'react-redux';

const DashboardPage = (props) => {
    const [hasFaq, setHasFaq] = useState(false);
    const dbContainer = props.match.params.name;

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
                              {
                                {
                                    'myorder' : <MyOrders />,
                                    'mywallet' : <MyWallet/>,
                                    'myservices' : <MyServices {...props} />,
                                    'mycourses' : <MyCourses/>
                                }[dbContainer]
                              }  
                            </div>
                        </div>
                    </div>
                </div>
                <FAQ setHasFaq={setHasFaq}/>
                <HaveQuery />
                <PopularCourses />
            </main>
            <Footer /> 
        </div>
    )
}

export default DashboardPage;