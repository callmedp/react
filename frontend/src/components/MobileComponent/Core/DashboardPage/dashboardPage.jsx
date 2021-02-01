
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
import { Helmet } from 'react-helmet';
import { fetchPopularServices } from 'store/CataloguePage/actions/index';

const Dashboard = (props) => {
    const dbContainer = props.match.params.name;
    const { history } = props;
    const dashboardRoutes = ['mycourses', 'myorder', 'mywallet', 'myservices']
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
        if(!dashboardRoutes.includes(dbContainer)){
            history.push('/404/');
        }
        handleEffects();
    }, [dbContainer])


    return(
        <div>
            <Helmet>
                <title>
                {
                    {
                        'myservices' : 'My Services | Shine Learning',
                        'mycourses' : 'My Courses | Shine Learning',
                        'myorder' : 'My Orders | Shine Learning',
                        'mywallet' : 'My Wallet | Shine Learning'
                    }[dbContainer]
                }
                </title>
            </Helmet>

            { showSearchPage ? <SearchPage setShowSearchPage={setShowSearchPage} /> :
                <>
                    <MenuNav />
                    <header className="m-container m-header pb-0">
                        <Header setShowSearchPage={setShowSearchPage} name='Dashboard' />
                        <DashboardNavigation activeTab={dbContainer}/>
                    </header>
                    <div className="m-container">
                        {
                            {
                                'myservices' : <MyServices />,
                                'mycourses' : <MyCourses/>,
                                'myorder' : <MyOrders />,
                                'mywallet' : <MyWallet/>
                            }[dbContainer]
                        }
                        
                        {/*<EditSkills />
                        <PersonalDetail /> */}
                        
                        <ProductCardsSlider productList={popularServices} />
                        <HaveQuery />
                    </div>
                    <Footer /> 
                </>
            }
        </div>
    )
}

export default Dashboard;