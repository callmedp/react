import React, { useEffect } from 'react';
import Header from '../../Common/Header/header';
import CatalogBanner from './Banner/banner';
import CoursesTray from './CoursesTray/coursesTray';
import AllCategories from './AllCategories/allCategories';
import ServicesForYou from './ServicesForYou/servicesForYou';
import RecentCourses from './RecentCourses/recentCourses';
import OurVendors from './OurVendors/ourVendors';
import Footer from 'components/DesktopComponent/Common/Footer/footer';
import './cataloguePage.scss';
import Aos from "aos";
// import "aos/dist/aos.css";
import { useDispatch, useSelector } from 'react-redux';
import MetaContent from '../../Common/MetaContent/metaContent';
import { fetchRecentlyAddedCourses, fetchPopularServices, 
    fetchAllCategoriesAndVendors, fetchTrendingCategories } from 'store/CataloguePage/actions/index';

const CatalogPage = (props) => {

    const dispatch = useDispatch();
    const meta_tags = useSelector((store) => store.allCategories.meta ? store.allCategories.meta : '');

    useEffect(() => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        //You may notice that apis corresponding to these actions are not getting called on initial render.
        //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
        //So there is no need to fetch them again on the browser.
        if (!(window && window.config && window.config.isServerRendered)) {
            new Promise((resolve, reject) => dispatch(fetchRecentlyAddedCourses({ resolve, reject })));
            new Promise((resolve, reject) => dispatch(fetchPopularServices({ resolve, reject })));
            new Promise((resolve, reject) => dispatch(fetchTrendingCategories({ 'medium': 0, resolve, reject })));
            new Promise((resolve, reject) => dispatch(fetchAllCategoriesAndVendors({ num: 8, resolve, reject })));
        }
        else {
            //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
            //above actions need to be dispatched.
            delete window.config?.isServerRendered
        }
    }, [])

    return (
        <>
            { meta_tags && <MetaContent meta_tags={meta_tags}/> }
            <div>
                <Header />
                <main>
                    <CatalogBanner />
                    <CoursesTray />
                    <AllCategories />
                    <ServicesForYou />
                    <RecentCourses />
                    <OurVendors />
                </main>
                <Footer />
            </div>
        </>
    )
}

export default CatalogPage;