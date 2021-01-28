import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './dashboardPage.scss';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import Footer from '../../Common/Footer/Footer';
import {default as ProductCardsSlider} from '../../Common/ProductCardsSlider/productCardsSlider';
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
import { fetchPopularServices } from 'store/CataloguePage/actions/index';

const Dashboard = (props) => {
    const dbContainer = props.match.params.name;
    const dispatch = useDispatch();
    const [showSearchPage, setShowSearchPage] = useState(false);
    const { popularServices } = useSelector(store => store?.popularServices );

    const handleEffects = async () => {
        if (!(window && window.config && window.config.isServerRendered)) {
            await new Promise((resolve, reject) => dispatch(fetchPopularServices({ resolve, reject })));
        }
        else {
            delete window.config?.isServerRendered
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
                        <Header setShowSearchPage={setShowSearchPage} name='Dashboard' />
                        <DashboardNavigation activeTab={dbContainer}/>
                    </header>
                    <main className="m-container">
                        {
                            {
                                'my-services' : <MyServices />,
                                'my-courses' : <MyCourses/>,
                                'my-orders' : <MyOrders />,
                                'my-wallet' : <MyWallet/>
                            }[dbContainer]
                        }
                        
                        {/*<EditSkills />
                        <PersonalDetail /> */}
                        
                        <ProductCardsSlider productList={popularServices} />
                        <HaveQuery />
                    </main>
                    <Footer /> 
                </>
            }
        </div>
    )
}

export default Dashboard;