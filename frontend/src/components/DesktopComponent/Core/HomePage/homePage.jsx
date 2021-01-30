import React, { useEffect } from 'react';
import OfferEnds from './OfferEnds/offerEnds';
import Header from '../../Common/Header/header';
import HomeBanner from './Banner/banner';
import PopularCourses from './PopularCourses/popularCourses';
import RecruitersLooking from './RecruitersLooking/recruitersLooking';
import ServicesForYou from './ServicesForYou/servicesForYou';
import MostViewedCourses from './MostViewedCourses/mostViewedCourses';
import LearningAdvantage from './LearningAdvantage/learningAdvantage';
import BoostedCareers from './BoostedCareers/boostedCareers';
import PracticeTestBanner from './PracticeTestBanner/practiceTestBanner';
import OurLearners from './OurLearners/ourLearners';
import LatestBlog from './LatestBlog/latestBlog';
import Footer from '../../Common/Footer/footer';
import '../CatalogPage/catalogPage.scss';
import Aos from "aos";
import "aos/dist/aos.css";

const HomePage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])
    return (
        <div>
            <OfferEnds />
            <Header />
            <main>
                <HomeBanner />
                <PopularCourses />
                <RecruitersLooking />
                <ServicesForYou />
                <MostViewedCourses />
                <LearningAdvantage />
                <BoostedCareers />
                <PracticeTestBanner />
                <OurLearners />
                <LatestBlog />
            </main>
            <Footer />
        </div>
    )
}

export default HomePage;