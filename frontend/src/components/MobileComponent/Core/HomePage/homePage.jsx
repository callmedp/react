import React, { useEffect } from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import OfferEnds from './OfferEnds/offerEnds';
import HomeBanner from './Banner/Banner';
import CareerGuidance from './CareerGuidance/careerGuidance';
import PopularCourses from './PopularCourses/popularCourses';
import UpgradeSkills from './UpgradeSkills/upgradeSkills';
import RecruitersLooking from './RecruitersLooking/recruitersLooking';
import ServicesForYou from './ServicesForYou/servicesForYou';
import MostViewedCourses from './MostViewedCourses/mostViewedCourses';
import LearningAdvantage from './LearningAdvantage/learningAdvantage';
import BoostedCareers from './BoostedCareers/boostedCareers';
import PracticeTestBanner from './PracticeTestBanner/practiceTestBanner';
import OurLearners from './OurLearners/ourLearners';
import LatestBlog from './LatestBlog/latestBlog';
import Footer from '../../Common/Footer/Footer';
// import CTAhome from '../../Common/CTA/CTAhome';
import Aos from "aos";
// import "aos/dist/aos.css";

const CatalogPage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])
    return (
        <div className="mb-100">
            {/* <OfferEnds /> */}
            <MenuNav />
            <header className="m-container m-header">
                <Header showSearchButton={false} icon={true} />
                <HomeBanner />
            </header>
            <CareerGuidance />
            <main className="mb-0">
                <PopularCourses />
                <UpgradeSkills />
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
            {/* <CTAhome /> */}
        </div>
    )
}

export default CatalogPage;