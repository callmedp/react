import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
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
import "aos/dist/aos.css";
import { fetchTestimonials } from 'store/HomePage/actions';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';

const HomePage = (props) => {

    const dispatch = useDispatch()
    const { homePageLoader } = useSelector(store => store.loader);

    const handleEffects = async () => {
        try {
                dispatch(startHomePageLoader());
                new Promise((resolve, reject) => dispatch(fetchTestimonials({resolve, reject})))
                dispatch(stopHomePageLoader());
            }
        catch{
            dispatch(stopHomePageLoader());
        }
    };

    useEffect( () => {
        handleEffects();
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <>
            { homePageLoader && <Loader /> }
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
        </>
    )
}

export default HomePage;