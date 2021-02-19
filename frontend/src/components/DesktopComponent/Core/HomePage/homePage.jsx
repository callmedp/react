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
import '../CataloguePage/cataloguePage.scss';
import Aos from "aos";
// import "aos/dist/aos.css";
import { useDispatch, useSelector } from 'react-redux';
import {
    fetchMostViewedCourses,
    fetchInDemandProducts,
    fetchJobAssistanceAndBlogs,
    fetchTestimonials,
} from 'store/HomePage/actions';
import Loader from '../../Common/Loader/loader';
import MetaContent from '../../Common/MetaContent/metaContent';


const HomePage = (props) => {

    const dispatch = useDispatch();
    const { homeLoader } = useSelector(store => store.loader)
    const { meta } = useSelector( store => store.testimonials )

    const handleEffect = async () => {
        //You may notice that apis corresponding to these actions are not getting called on initial render.
        //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
        //So there is no need to fetch them again on the browser.
        if (!(window && window.config && window.config.isServerRendered)) {
            try {
                new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({ payload:{categoryId: -1}, resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ payload: {pageId: 1, tabType: 'master', device: 'desktop'}, resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchJobAssistanceAndBlogs({ resolve, reject })));
                new Promise((resolve, reject) => dispatch(fetchTestimonials({ payload:{device: 'desktop'}, resolve, reject })));
            }
            catch (err) {
                console.log("error occured at Homepage", err)
            }
        }
        else {
            // isServerRendered is needed to be deleted because when routing is done through react and not on the node,
            // above actions need to be dispatched.
            delete window.config?.isServerRendered
        }
    }

    useEffect(() => {

        handleEffect()

        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <div>
            { meta && <MetaContent meta_tags={meta}/> }
            { homeLoader ? <Loader /> : ''}
            {/* <OfferEnds /> */}
            <Header isHomepage={true} />
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
            <Footer homepage={true} />
        </div>
    )
}

export default HomePage;