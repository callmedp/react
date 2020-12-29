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
import './catalogPage.scss';
import Aos from "aos";
import "aos/dist/aos.css";

const CatalogPage = (props) => {
    const [showSearchPage, setShowSearchPage] = useState(false)

    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <div>
            { 
                showSearchPage ? 
                <SearchPage setShowSearchPage={setShowSearchPage} /> :
                <>
                    <MenuNav />
                    <header className="m-container m-header">
                        <Header setShowSearchPage={setShowSearchPage} />
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