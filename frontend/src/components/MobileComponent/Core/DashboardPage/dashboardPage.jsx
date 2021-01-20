import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './dashboardPage.scss';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import Footer from '../../Common/Footer/Footer';
import PopularCoursesSlider from '../../Common/ProductCardsSlider/productCardsSlider';
import HaveQuery from './HaveQuery/haveQuery';
import DashboardNavigation from './DashboardNavigation/dashboradNav';
import MyCourses from './MyCourses/myCourses';
import MyServices from './MyServices/myServices';
import MyOrders from './MyOrders/myOrders';
import MyWallet from './MyWallet/myWallet';
import MyProfile from './MyProfile/myProfile';
import PersonalDetail from './MyProfile/PersonalDetail';
import EditSkills from './MyProfile/EditSkills';
import SearchPage from '../../Common/SearchPage/SearchPage';
import { fetchMyOrders } from 'store/DashboardPage/MyOrder/actions/index';
import { fetchMyWallet } from 'store/DashboardPage/MyWallet/actions/index';

const Dashboard = () => {
    const [showSearchPage, setShowSearchPage] = useState(false);
    const [activeTab, setActiveTab] = useState('Courses');

    const dispatch = useDispatch();
    // const { history } = props;
    // const { walletLoader } = useSelector(store => store.loader);

    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                new Promise((resolve, reject) => dispatch(fetchMyOrders({ page: 1, resolve, reject })))
                await new Promise((resolve, reject) => dispatch(fetchMyWallet({ page: 1, resolve, reject })))
            }
            else {
                //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
                //above actions need to be dispatched.
                delete window.config?.isServerRendered
            }
        } catch (error) {
            // if (error?.status == 404) {
            //     history.push('/404');
            // }
        }
    };

    useEffect(() => {
        handleEffects();
    }, [])

    return(
        <div>
            { showSearchPage ? <SearchPage setShowSearchPage={setShowSearchPage} /> :
                <>
                    <MenuNav />
                    <header className="m-container m-header pb-0">
                        <Header setShowSearchPage={setShowSearchPage} />
                        <DashboardNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
                    </header>
                    <main className="m-container">
                        { activeTab === 'Courses' && <MyCourses /> }
                        { activeTab === 'Services' && <MyServices /> }
                        { activeTab === 'Orders' && <MyOrders /> }
                        { activeTab === 'Wallet' && <MyWallet /> }
                        { activeTab === 'Profile' && <MyProfile /> }
                        
                        {/*<EditSkills />
                        <PersonalDetail /> */}
                        
                        <PopularCoursesSlider />
                        <HaveQuery />
                    </main>
                    <Footer /> 
                </>
            }
        </div>
    )
}

export default Dashboard;