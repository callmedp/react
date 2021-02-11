import React, { useEffect, useState } from 'react';
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
import CTAhome from '../../Common/CTA/CTAhome';
import Aos from "aos";
import "aos/dist/aos.css";
import { fetchTestimonials, fetchJobAssistanceAndBlogs, fetchMostViewedCourses, fetchInDemandProducts } from 'store/HomePage/actions';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions/index';
import Loader from '../../Common/Loader/loader';
import SearchPage from '../../Common/SearchPage/SearchPage'
import './homePage.scss';

const HomePage = (props) => {

    const dispatch = useDispatch()
    const { homeLoader } = useSelector( store => store.loader )
    const [showSearch, setShowSearch] = useState(false)
    const [stickSearchBar, showStickSearchBar] = useState(false)

    const handleEffects = async () => {
        try {
                dispatch(startHomePageLoader());
                new Promise((resolve, reject) => dispatch(fetchTestimonials({resolve, reject})))
                new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({categoryId: -1, resolve, reject})))
                new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ pageId: 1, tabType: 'master', device:'mobile', resolve, reject})));
                await new Promise((resolve, reject) => dispatch(fetchJobAssistanceAndBlogs({resolve, reject})))
                dispatch(stopHomePageLoader());
            }
        catch{
            dispatch(stopHomePageLoader());
        }
    };

    const handleScroll=() => {
        const offset = window.scrollY;
        if(offset > 140 ) {
            showStickSearchBar(true)
        }
        else showStickSearchBar(false)
    }

    useEffect( () => {
        handleEffects();
        window.addEventListener('scroll', handleScroll);
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <>
            { homeLoader && <Loader /> }
            {
                showSearch ? <SearchPage setShowSearchPage={setShowSearch} /> :
                    <div className="mb-100">
                        {/* <OfferEnds /> */}
                        <MenuNav />
                        <header className="m-container m-header">
                            <Header showSearchButton={false} icon={true} />
                            <HomeBanner setShowSearch={setShowSearch} />
                        </header>
                        {/* <CareerGuidance /> */}
                        {
                            stickSearchBar && 
                                <div className="stick-search-header" onClick={() => setShowSearch(true)} data-aos='fade-down'>
                                    <SearchPage crossSearch={false} />
                                </div>
                        }
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
                        <Footer pageType='homePage'/>
                        <CTAhome />
                    </div>
            }
        </>
    )
}

export default HomePage;