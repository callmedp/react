import React, { useEffect } from 'react';
import Header from '../../Common/Header/header';
import CatalogBanner from './Banner/banner';
import CoursesTray from './CoursesTray/coursesTray';
import AllCategories from './AllCategories/allCategories';
import ServicesForYou from './ServicesForYou/servicesForYou';
import RecentCourses from './RecentCourses/recentCourses';
import OurVendors from './OurVendors/ourVendors';
import Footer from '../../Common/Footer/footer';
import './cataloguePage.scss';
import Aos from "aos";
import "aos/dist/aos.css";

const CatalogPage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])
    return (
        <div>
            <Header />
            <main>
                <CatalogBanner />
                {/* <CoursesTray /> */}
                <AllCategories />
                <ServicesForYou />
                <RecentCourses />
                <OurVendors />
            </main>
            <Footer />
        </div>
    )
}

export default CatalogPage;