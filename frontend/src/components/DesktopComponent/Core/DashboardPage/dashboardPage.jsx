import React, {useState, useEffect} from 'react';
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
import { useDispatch, useSelector } from 'react-redux';
import {fetchMyWallet} from 'store/DashboardPage/MyWallet/actions';
import { startSkillPageLoader, stopSkillPageLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';

const DashboardPage = (props) => {
    const [hasFaq, setHasFaq] = useState(false);
    const pageId = props.match.params.id;
    const dispatch = useDispatch();
    const { history } = props;
    const { skillLoader } = useSelector(store => store.loader);

    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startSkillPageLoader());
                new Promise((resolve, reject) => dispatch(fetchMyWallet({ id: pageId, resolve, reject })))
                dispatch(stopSkillPageLoader());
            }
            else {
                //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
                //above actions need to be dispatched.
                delete window.config?.isServerRendered
            }
        } catch (error) {
            if (error?.status == 404) {
                history.push('/404');
            }
        }
    };

    useEffect(() => {
        handleEffects();
    }, [pageId])

    return(
        <div>
           { skillLoader ? <Loader /> : ''}

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
                                <MyWallet />
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