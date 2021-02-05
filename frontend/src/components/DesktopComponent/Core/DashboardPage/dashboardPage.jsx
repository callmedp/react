import React, { useState, useEffect } from 'react';
import './dashboardPage.scss';
import Header from '../../Common/Header/header';
import Footer from '../../Common/Footer/footer';
import PopularCourses from './PopularCourses/PopularCourses';
import DashboardNavigation from './DashboardNavigation/DashboardTabs';
import HaveQuery from './HaveQuery/HaveQuery';
// import BreadCrumbs from './Breadcrumb/Breadcrumb';
import MyCourses from './MyCourses/myCourses';
import MyServices from './MyServices/myServices';
import MyOrders from './MyOrders/myOrders';
import MyWallet from './MyWallet/myWallet';
import MyProfile from './MyProfile/myProfile';
import FAQ from './FAQ/faq';
import { Helmet } from 'react-helmet';
// import { useDispatch, useSelector } from 'react-redux';
import StartCourse from './StartCourse/startCourse';

const DashboardPage = (props) => {
    const [hasFaq, setHasFaq] = useState(false);
    const { history } = props;
    const dbContainer = props.match.params.name;
    const dashboardRoutes = [undefined, 'myorder', 'mywallet', 'myservices', 'startcourse']
    
    useEffect(()=>{
        if(!dashboardRoutes.includes(dbContainer)){
            history.push('/404/');
        }
    },[dbContainer])

    return(
        <div>
            <Helmet>
                <title>
                {
                    {
                        'myservices' : 'My Services | Shine Learning',
                        'mycourses' : 'My Courses | Shine Learning',
                        'myorder' : 'My Orders | Shine Learning',
                        'mywallet' : 'My Wallet | Shine Learning',
                        'startcourse' : 'Start Course | Shine Learning'
                    }[dbContainer]
                }
                </title>
            </Helmet>
           <Header />
           <main>
                <div className="container">
                    {/* <BreadCrumbs /> */}
                    
                    <div className="dashboard-warp">
                        { dbContainer != 'startcourse' ?
                        <div className="dashboard-warp--tab">
                         <DashboardNavigation /> 
                        </div>: '' }

                        {dbContainer != 'startcourse' ?
                        <div className="dashboard-warp--wrap">
                            <div className="dashboard-warp--content">
                              {
                                {
                                    'myorder' : <MyOrders />,
                                    'mywallet' : <MyWallet/>,
                                    'myservices' : <MyServices {...props} />,
                                    undefined : <MyCourses history={history} />
                                }[dbContainer]
                              }  
                            </div>
                        </div>: '' }
                        {
                            {
                                'startcourse' : <StartCourse />,
                            }[dbContainer]
                        }  
                    </div>
                </div>
                { dbContainer === 'mywallet' ? <FAQ setHasFaq={setHasFaq}/> : '' }
                { dbContainer != 'startcourse' ? <HaveQuery /> : '' }
                { dbContainer != 'startcourse' ? <PopularCourses /> : '' }
            </main>
            <Footer /> 
        </div>
    )
}

export default DashboardPage;