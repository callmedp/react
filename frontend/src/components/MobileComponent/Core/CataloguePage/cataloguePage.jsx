import React, { useEffect, useState } from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import CatalogBanner from './Banner/Banner';
import RecommendedCourses from './RecommendedCourses/recommendedCourses';
import AllCategories from './AllCategories/allCategories';
import ServicesForYou from './ServicesForYou/servicesForYou';
import RecentCourses from './RecentCourses/recentCourses';
import OurVendors from './OurVendors/ourVendors';
import Footer from '../../Common/Footer/Footer';
import SearchPage from '../../Common/SearchPage/SearchPage';
import './cataloguePage.scss';
import Aos from "aos";
// import "aos/dist/aos.css";
import { useDispatch, useSelector } from 'react-redux';
import {
    fetchRecentlyAddedCourses,
    fetchPopularServices,
    fetchTrendingCategories,
    fetchAllCategoriesAndVendors
} from 'store/CataloguePage/actions/index';
import MetaContent from '../../Common/MetaContent/metaContent';

const CatalogPage = (props) => {
    const [showSearchPage, setShowSearchPage] = useState(false)
    const dispatch = useDispatch();
    const meta_tags = useSelector((store) => store.allCategories.meta ? store.allCategories.meta : '');

    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        new Promise((resolve, reject) => dispatch(fetchRecentlyAddedCourses({ resolve, reject })));
        new Promise((resolve, reject) => dispatch(fetchPopularServices({ resolve, reject })));
        new Promise((resolve, reject) => dispatch(fetchTrendingCategories({ 'medium': 1, resolve, reject })));
        new Promise((resolve, reject) => dispatch(fetchAllCategoriesAndVendors({ num:8, resolve, reject })));
    }, [])

    return (
        <div>
            { meta_tags && <MetaContent meta_tags={meta_tags}/> }
            { 
                showSearchPage ? 
                <SearchPage setShowSearchPage={setShowSearchPage} /> :
                <>
                    <MenuNav />
                    <header className="m-container m-header">
                        <Header setShowSearchPage={setShowSearchPage} hideName={true}/>
                        <CatalogBanner />
                    </header>
                    <main className="mb-0">
                        <RecommendedCourses />
                        <AllCategories />
                        <ServicesForYou />
                        <RecentCourses />
                        <OurVendors />
                    </main>
                    <Footer />
                </>
            }
        </div>
    )
}

export default CatalogPage;